import unittest
from model.User import User
from service.Service import Service
from repository.Repository import Repository


# class TestUserRepository(unittest.TestCase):
    # def setUp(self):
    #     self.repository = Repository()
    #     self.inserted_User_id = self.UserRepository.insert(User(None, "acctnum", 1, 25.00))

    # def tearDown(self):
    #     self.UserRepository.delete(User(int(self.inserted_User_id),"",1,0.0))

    # def test_get(self):
    #     get_User: User = self.UserRepository.get(
    #         self.inserted_User_id)
    #     self.assertEqual(get_User.id, int(self.inserted_User_id))

    # def test_update(self):
    #     get_User: User = self.UserRepository.get(
    #         self.inserted_User_id)
    #     balance_update_check = 15.00
    #     get_User.updateBalance(balance_update_check)
    #     self.UserRepository.update(get_User)
    #     updated_User: User = self.UserRepository.get(self.inserted_User_id)
    #     self.assertEqual(updated_User, get_User)

# if __name__ == "__main__":
#     unittest.main()