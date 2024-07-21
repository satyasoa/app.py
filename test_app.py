import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_principal_assignments(self):
        headers = {"X-Principal": {"user_id": 5, "principal_id": 1}}
        response = self.app.get("/principal/assignments", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], [{"id": 1, "content": "ESSAY T1", "grade": None, "state": "SUBMITTED"}])

    def test_get_principal_teachers(self):
        headers = {"X-Principal": {"user_id": 5, "principal_id": 1}}
        response = self.app.get("/principal/teachers", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], [{"id": 1, "user_id": 3}])

    def test_grade_assignment(self):
        headers = {"X-Principal": {"user_id": 5, "principal_id": 1}}
        payload = {"id": 1, "grade": "A"}
        response = self.app.post("/principal/assignments/grade", headers=headers, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], {"id": 1, "content": "ESSAY T1", "grade": "A", "state": "GRADED"})

if __name__ == "__main__":
    unittest.main()
