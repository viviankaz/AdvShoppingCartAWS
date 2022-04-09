import unittest
import adshopcart_methods as methods
import adshopcart_locators as locators


class AOSPositiveTestCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        methods.setUp()

    @classmethod
    def tearDownClass(cls):
        methods.tearDown()

    def setUp(self):
        print('\n===== Test started:', self.shortDescription())

    def tearDown(self):
        print('===== Test finished:', self.shortDescription())

    @staticmethod
    def test_homepage():
        """Test Homepage of Advantage Online Shopping Cart App"""
        methods.check_categories()
        methods.check_top_navi_menu()
        methods.check_main_logo()
        methods.check_contact_form()

    @staticmethod
    def test_signup_and_delete():
        """Test Sign up and Delete of Advantage Online Shopping Cart App"""
        methods.register_new_account()
        methods.check_new_user_info()
        methods.sign_out()
        methods.sign_in_with_right_credentials(locators.user_name, locators.password)
        methods.delete_account()
        methods.sign_in_with_wrong_credentials(locators.user_name, locators.password)


