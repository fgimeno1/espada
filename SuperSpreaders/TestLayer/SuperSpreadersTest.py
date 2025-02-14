import unittest
from parameterized import parameterized
from numpy import array, ndarray, concatenate
from numpy.linalg import eigh, norm
import asyncio
from datetime import datetime

# Importing principal methods
from SuperSpreaders.BusinessLayer.graphModelService import _isRiskyMovement
from SuperSpreaders.BusinessLayer.graphModelService import _takingTheConnectedComponents
from SuperSpreaders.BusinessLayer.graphModelService import _takeRiskyMovementsBetweenFarms
from SuperSpreaders.BusinessLayer.graphModelService import _performingAdjacencyMatrix
from SuperSpreaders.BusinessLayer.graphModelService import _takingSuperSpreaders

# Importing DTOs
from SuperSpreaders.Shared.DTOs import MovementDTO


class SuperSpreaderTest(unittest.TestCase):


    @parameterized.expand(
            [["case_1", 1, 1, False],
            ["case_2", 1, 2, False],
            ["case_3", 1, 3, False],
            ["case_4", 2, 1, True],
            ["case_5", 2, 2, False],
            ["case_6", 2, 3, False],
            ["case_7", 3, 1, True],
            ["case_8", 3, 2, True],
            ["case_9", 3, 3, False]]
    )
    def test_isRisky(self, name, inicio, fin, resultado):
        self.assertEqual(_isRiskyMovement(inicio, fin), resultado)

    @parameterized.expand(
        [["case_1", 
          array([1,2,3,4,5,6,7]), 
          array([
              [0,1,0,1,0,0,0],
              [1,0,1,0,0,0,0],
              [0,1,0,0,0,0,0],
              [1,0,0,0,0,0,0],
              [0,0,0,0,0,1,1],
              [0,0,0,0,1,0,0],
              [0,0,0,0,1,0,0]
          ])]]
    )
    def test_TakingTheConnectedComponents(self, name, indexes, matrix):
        self.assertEqual(len(_takingTheConnectedComponents(indexes, matrix)), 2)

    @parameterized.expand(
            [
                ["case_0", 43, datetime(day=1, month=12, year=2024), datetime(day=31, month=12, year=2024)]
            ]
    )
    def test_TakeRiskyMovementsBetweenFarms(self, name : str, company : int, beginDate : datetime, endDate : datetime):
        result : list[MovementDTO] = asyncio.run(_takeRiskyMovementsBetweenFarms(empresa=company,
                                                             fechaComienzo=beginDate,
                                                             fechaFin=endDate))
        
        
        # Comprobamos que todos los movimientos sean de riesgo
        self.assertTrue(all(map(lambda x : x.BeginCenterSubclasificationId > x.EndCenterSubclasificationId, result)))

        # Comprobamos que todos los movimientos se hayan hecho en la misma fecha
        self.assertTrue(all(map(lambda x : x.StartDatetime.date() == x.EndDatetime.date(), result)))

        # Comprobamos que el centro de destino sea distinto al centro de llegada
        self.assertTrue(all(map(lambda x : x.BeginCenterId != x.EndCenterId, result)))

    @parameterized.expand(
        [
            ["case_0",
             [
                 MovementDTO(BeginCenterId=1,
                             EndCenterId=2,
                             BeginCenterSubclasificationId=1,
                             EndCenterSubclasificationId=1,
                             StartDatetime=datetime(day=1, month=12, year=2024),
                             EndDatetime=datetime(day=1, month=12, year=2024),
                             VehicleId=1),
                MovementDTO(BeginCenterId=1,
                             EndCenterId=3,
                             BeginCenterSubclasificationId=1,
                             EndCenterSubclasificationId=1,
                             StartDatetime=datetime(day=1, month=12, year=2024),
                             EndDatetime=datetime(day=1, month=12, year=2024),
                             VehicleId=1)
             ]]
        ]
    )
    def test_PerformingAdjacentMatrix(self, name : str, riskyMovements : list[MovementDTO]):
        
        centers_id, matrix = _performingAdjacencyMatrix(riskyMovements)

        self.assertTrue((array([1,2,3]) == centers_id).all())
        self.assertTrue((array([[0,1,1],[1,0,0],[1,0,0]]) == matrix).all())

    @parameterized.expand(
        [
            [
                "case_0",
                array([1,2,3,4,5,6,7]), 
                array([
                    [0,1,0,1,0,0,0],
                    [1,0,1,0,0,0,0],
                    [0,1,0,0,0,0,0],
                    [1,0,0,0,0,0,0],
                    [0,0,0,0,0,1,1],
                    [0,0,0,0,1,0,0],
                    [0,0,0,0,1,0,0]
                ]),
                [{1,2,3,4}, {5,6,7}]
            ]
        ]
    )
    def test_TakingSuperSpreaders(self, name, centers_id : ndarray, adj_matrix : ndarray, components : list[set[int]]):

        eigenvalueCentrality = _takingSuperSpreaders(centers_id, adj_matrix, components)
        
        adj_mat_1 = adj_matrix[0:4, 0:4]
        adj_mat_2 = adj_matrix[4:7, 4:7]

        eigenvalue_1, eigenvector_1 = eigh(adj_mat_1)
        eigenvalue_2, eigenvector_2 = eigh(adj_mat_2)

        ind_1 = eigenvalue_1.argmax()
        ind_2 = eigenvalue_2.argmax()

        eigenvector_1 = abs(eigenvector_1[:, ind_1]) / norm(eigenvector_1[:, ind_1])
        eigenvector_2 = abs(eigenvector_2[:, ind_2]) / norm(eigenvector_2[:, ind_2])

        centrality = concatenate([eigenvector_1, eigenvector_2])

        self.assertTrue((eigenvalueCentrality == centrality).all())

