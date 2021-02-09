


import os
import app
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        with app.app.app_context():
            app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])
    
    # def test_url(self):
    #     print('\n')
    #     tester = self.app
    #     try:
    #         url='https://www.nytimes.com/2021/01/09/us/politics/trump-impeachment-possible.html'
    #         response = tester.post(
    #         '/detect',
    #         data = dict(name='https://www.nytimes.com/2021/01/09/us/politics/trump-impeachment-possible.html'),
    #         follow_redirects=True
    #         )
    #         print("success-",url)
    #         print('\n')
    #     except:
    #         print("error-",url)
    #         print('\n')

    #     try:
    #         url='https://timesofindia.indiatimes.com/blogs/toi-editorials/toughest-budget-fm-has-to-lay-a-road-map-for-recovering-from-the-vast-damage-of-last-year/'
    #         response = tester.post(
    #         '/detect',
    #         data = dict(name='https://timesofindia.indiatimes.com/blogs/toi-editorials/toughest-budget-fm-has-to-lay-a-road-map-for-recovering-from-the-vast-damage-of-last-year/'),
    #         follow_redirects=True
    #         )
    #         print("success-",url)
    #         print('\n')

    #     except:
    #         print("error-",url)
    #         print('\n')
    #     try:
    #         url='https://www.foxnews.com/politics/trump-acknowledged-he-bears-some-blame-for-capitol-riot-last-week-in-call-with-mccarthy-sources'

    #         response = tester.post(
    #         data = dict(name='https://www.foxnews.com/politics/trump-acknowledged-he-bears-some-blame-for-capitol-riot-last-week-in-call-with-mccarthy-sources'),
    #         follow_redirects=True
    #         )
    #         print("success-",url)
    #         print('\n')
    #     except:
    #         print("error-",url)
    #         print('\n')



        



if __name__ == '__main__':
    unittest.main()