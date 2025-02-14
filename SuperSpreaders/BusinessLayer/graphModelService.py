import pandas as pd
import numpy as np
from numpy.linalg import eigh, norm
from datetime import datetime

# Importing DTOs
from SuperSpreaders.Shared.DTOs import RegistroVisitaDTO, MovementDTO, CentroDTO

# Importing DAOs
from External.DataLayer.DAOs import asyncGetAllVehicleRegistroVisitaInfoByParameters
from RepComun.DataLayer.DAOs.CentroDAO import asyncGetCentroByEmpresa


async def _takeRiskyMovementsBetweenFarms(empresa : int | None = None,
                                soloActivos : bool | None = None,
                                fechaComienzo : datetime | None = None,
                                fechaFin : datetime | None = None) -> list[MovementDTO]:
    
    """
    The function connects with the BioExternal and RepComun BBDD and return a list with the risky movements
    associated to the input parameters.

    PARAMETERS
    ----------
        empresa : `int | None`
            Id of the company to be analyzed. If it is null, all the companies will be analyzed
        
        soloActivos : `bool | None`
            True for analyse only the active centers, False otherwise.

        fechaComienzo : `datetime | None`
            All the analysis will be performed since this date (included). If it is null, the analysis without a begining 
            restriction.

        fechaFin : `datetime | None`
            All the analysis will be performed until this date (included). If it is null, the analysis without an end 
            restriction.

    RETURN
    ------
        result : `list[MovementDTO]`
            A list of `MovementDTO` objects with all the risky movements associated to the domain parameters.
    """

    # Fetching visits from DB
    visits = await asyncGetAllVehicleRegistroVisitaInfoByParameters(None, soloActivos, fechaComienzo, fechaFin)
    centers = await asyncGetCentroByEmpresa(empresa)

    # Filtering only with the society required
    visitsDTO = RegistroVisitaDTO.mapRegistroVisitaInfoToDTO(visits)
    centersDTO = CentroDTO.mapCentroToDTO(centers)

    # Freeing space from memory
    del visits, centers

    visitsDF = pd.DataFrame(visitsDTO)
    centersDF = pd.DataFrame(centersDTO).filter(items=["Id"])

    visitsA = pd.merge(visitsDF, centersDF, left_on="IdCentro", right_on="Id", how="inner")

    # Freeing space from memory
    del visitsDTO, centersDTO, centersDF, visitsDF

    # Performing the movements between farms
    visitsA.sort_values(by=["Fecha", "IdVehiculo"], inplace=True)
    visitsB = visitsA.copy().tail(-1).reset_index()
    visitsA = visitsA.head(-1).reset_index()

    ## Making different names for the columns values
    visitsA.columns = list(map(lambda x : x + "A", visitsA.columns))
    visitsB.columns = list(map(lambda x : x + "B", visitsB.columns))

    ## Joining both dataframes
    movements = pd.concat([visitsA, visitsB], axis=1)
    del visitsA, visitsB

    ## Filtering both dataframes to perform the visits
    movements = movements[movements["IdCentroA"] != movements["IdCentroB"]]
    movements = movements[movements["IdVehiculoA"] == movements["IdVehiculoB"]]
    movements = movements[movements["FechaA"].dt.date == movements["FechaB"].dt.date]

    ## Filtering movements by risky or not risky
    movements["Risky"] = movements.apply(lambda x : _isRiskyMovement(x["IdTipoSubclasificacionA"], x["IdTipoSubclasificacionB"]), axis=1)
    movements = movements[movements["Risky"]]

    return map(lambda x : MovementDTO(BeginCenterId=x["IdCentroA"],
                                      EndCenterId=x["IdCentroB"],
                                      BeginCenterSubclasificationId=x["IdTipoSubclasificacionA"],
                                      EndCenterSubclasificationId=x["IdTipoSubclasificacionB"],
                                      StartDatetime=x["FechaA"],
                                      EndDatetime=x["FechaB"],
                                      VehicleId=x["IdVehiculoA"]),
               movements.to_dict(orient="records"))

def _isRiskyMovement(idSubclasificacionStart : int, idSubclasificacionEnd : int) -> bool:

    if (idSubclasificacionStart == 3) and ((idSubclasificacionEnd) == 1 or (idSubclasificacionEnd == 2)):
        return True
    elif (idSubclasificacionStart == 2) and (idSubclasificacionEnd == 1):
        return True
    else:
        return False
    
def _performingAdjacencyMatrix(movements : list[MovementDTO]) -> tuple[np.ndarray, np.ndarray]:
    
    # Taking all the centers Id
    centers_id = list()# = pd.Series(map(lambda x : x.BeginCenterId, movements), map(lambda x : x.EndCenterId, movements)).unique().sort()
    centers_id = centers_id + list(map(lambda x : x.BeginCenterId, movements))
    centers_id = centers_id + list(map(lambda x : x.EndCenterId, movements))
    centers_id = pd.Series(centers_id).unique()
    centers_id.sort()

    # Performing the adjacency matrix
    adj_matrix = pd.DataFrame(data = 0, columns=centers_id, index=centers_id)

    for movement in movements:
        adj_matrix.loc[movement.BeginCenterId, movement.EndCenterId] = adj_matrix.loc[movement.BeginCenterId, movement.EndCenterId] + 1

    adj_matrix = adj_matrix.to_numpy()

    return centers_id, adj_matrix + np.transpose(adj_matrix)

def _takingTheConnectedComponents(centers_id : np.ndarray, adj_matrix : np.ndarray) -> list[set[int]]:

    """
        Given the list of nodes and the adjacency matrix of a graph, this method compute the connected components.
        IMPORTANT: The nodes must have the same order in the `centers_id` and in the matrix `adj_matrix`, i.e. 
        if `adj_matrix[0,2] = 1`, then there exists a relation from the node `centers_id[0]`

        PARAMETERS
        ----------
            - centers_id : `ndarray`
                The vector with the nodes of the graph
            - adj_matrix : `ndarray`
                The adjacency matrix of the graph.

        RETURN
        ------
            - components : `list[set[int]]`
                This list represent the component list. Every element of the list is a set of integers, and every integer of the 
                set represent one of the graph nodes.
    """        

    relations : list[dict] = [] # List of relations between nodes. Each relation is an dictionary with two parameters, "From" and "To"
    adj_matrix_DF = pd.DataFrame(data=adj_matrix, columns=centers_id, index=centers_id) # DataFrame of the adj matrix to make easier the search
    components : list[set[int]] = [] # List where the components are saved

    # Filling the "relations" dataframe
    for x in centers_id:
        aux_index = adj_matrix_DF[adj_matrix_DF[x] != 0].index.to_list()

        for i in aux_index:
            relations.append({"From" : x, "To" : i})

    # Mapping the list relations to DataFrame to work easily
    relations_DF : pd.DataFrame = pd.DataFrame(relations)

    
    # Mientras queden relaciones la lista de relaciones
    while(relations_DF.shape[0] != 0):

        # Reseteamos la componente auxiliar
        aux_component = set()

        # Tomamos el "From" del primer elemento del dataframe y le 
        aux_index = relations_DF.iloc[0]["From"]
        aux_component.add(aux_index)

        # Mientras queden relaciones en las que el elemento "From" pertenezca al conjunto
        # aux_component, ejecutamos este bucle
        while(relations_DF["From"].isin(aux_component).any()):
            
            # Guardamos los nodos relacionados con los nodos de la componentes en aux_centers
            aux_centers = relations_DF[relations_DF["From"].isin(aux_component)]["To"].to_list()
            
            # Eliminamos de la lista de relaciones, adj_matrix_DF, aquellas que comienzan por los nodos del conjunto aux_component
            relations_DF = relations_DF[~relations_DF["From"].isin(aux_component)]

            # Añadimos los nodos de aux_centers al conjunto aux_component
            aux_component.update(aux_centers)

        # Actualizamos la lista de componentes, "components"
        components.append(aux_component)



    ## Devolvemos las componentes
    return components

def _takingSuperSpreaders(centers_id : np.ndarray, adj_matrix : np.ndarray, components : list[set[int]]) -> list[np.ndarray]:
    
    # Parsing adj_matrix to dataframe
    adj_matrix_DF = pd.DataFrame(data = adj_matrix, columns=centers_id, index=centers_id)
    
    # Container to save centralities
    centralities = pd.Series(data = 0.0, index=centers_id)

    # For every component the eigenvalue centrality must be calculated
    for component in components:
        aux_mat = adj_matrix_DF.loc[list(component), list(component)].to_numpy()

        eigenvalues, eigenvectors = eigh(aux_mat)
        
        # Finding the strictly dominant eigenvalue
        index_dominant_eigenvalue = eigenvalues.argmax()
        dominant_eigenvector = abs(eigenvectors[:,index_dominant_eigenvalue]) / norm(eigenvectors[:,index_dominant_eigenvalue])

        for i, v in zip(component, dominant_eigenvector):
            centralities[i] = v

    return centralities.to_numpy()
    

