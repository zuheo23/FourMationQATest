import unittest
import os
from selenium import webdriver
import time
import re
from selenium.webdriver.common.keys import Keys



url = 'https://m.kss.com.au/boxshop/'


'''
US-1
'''
class TestModifyQuantity(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.browser = webdriver.Chrome(executable_path='%s' % os.path.join(dir_path, 'chromedriver.exe'))
        self.browser.get(url)

    def test_up_arrow_increment_quantity(self):
        start_value = self.browser.find_elements_by_class_name('boxshop-item-input')[0].get_attribute('value')
        self.browser.find_elements_by_class_name('fa-chevron-up')[0].click()
        end_value = self.browser.find_elements_by_class_name('boxshop-item-input')[0].get_attribute(
            'value')
        self.assertEqual(int(end_value), (int(start_value) + 1))

    def test_down_arrow_decrement_quantity(self):
        start_value = self.browser.find_elements_by_class_name('boxshop-item-input')[0].get_attribute('value')
        self.browser.find_elements_by_class_name('fa-chevron-up')[0].click()
        self.browser.find_elements_by_class_name('fa-chevron-down')[0].click()
        self.browser.find_elements_by_class_name('fa-chevron-down')[0].click()
        end_value = self.browser.find_elements_by_class_name('boxshop-item-input')[0].get_attribute(
            'value')
        self.assertEqual(int(end_value), int(start_value))
        self.assertGreaterEqual(int(end_value), 1)

    def test_changing_quantity_via_textbox(self):
        # alphabet
        self.browser.find_elements_by_class_name('boxshop-item-input')[0].send_keys(Keys.BACKSPACE, 'abc' + Keys.TAB)
        end_value = self.browser.find_elements_by_class_name('boxshop-item-input')[0].get_attribute('value')
        self.assertEqual(end_value,'')

        # symbol
        self.browser.find_elements_by_class_name('boxshop-item-input')[0].send_keys(Keys.BACKSPACE, '@' + Keys.TAB)
        end_value = self.browser.find_elements_by_class_name('boxshop-item-input')[0].get_attribute('value')
        self.assertEqual(end_value, '')

        # numeric
        value = 23
        self.browser.find_elements_by_class_name('boxshop-item-input')[0].send_keys(Keys.BACKSPACE,  str(value) + Keys.TAB)
        end_value = self.browser.find_elements_by_class_name('boxshop-item-input')[0].get_attribute('value')
        self.assertEqual(int(end_value), value)

    def tearDown(self):
        self.browser.quit()

'''
US-2
'''
class TestAddToCart(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.browser = webdriver.Chrome(executable_path='%s' % os.path.join(dir_path, 'chromedriver.exe'))
        self.browser.get(url)

    def test_add_product_quantity_more_than_ten_to_cart(self):
        product_name = self.browser.find_element_by_class_name('boxshop-item-title').text
        quantity = 23
        price = 5.1
        total = float(quantity) * price

        self.browser.find_element_by_class_name('boxshop-item-input').send_keys(Keys.BACKSPACE + str(quantity) + Keys.TAB)
        self.browser.find_element_by_class_name('boxshop-item-add').click()
        time.sleep(5)
        self.browser.find_element_by_class_name('basket-toggle').click()

        e = self.browser.find_element_by_class_name('basket-item')

        tds = e.find_elements_by_tag_name('td')

        self.assertEqual(product_name.strip(), tds[1].text.strip())
        end_quantity = self.browser.find_element_by_class_name('boxshop-item-input').get_attribute('value')
        el = self.browser.find_element_by_class_name('basket-total')

        basket_total_pattern = 'Total\s+\$(\d+.\d+)'
        m = re.search(basket_total_pattern,el.text)
        basket_total = m.group(1)
        self.assertEqual(total, float(basket_total))

    def test_add_product_quantity_less_than_ten_to_cart(self):
        product_name = self.browser.find_element_by_class_name('boxshop-item-title').text
        quantity = 8
        price = 6.4
        total = float(quantity) * price

        self.browser.find_element_by_class_name('boxshop-item-input').send_keys(Keys.BACKSPACE + str(quantity) + Keys.TAB)
        self.browser.find_element_by_class_name('boxshop-item-add').click()
        time.sleep(5)
        self.browser.find_element_by_class_name('basket-toggle').click()

        e = self.browser.find_element_by_class_name('basket-item')

        tds = e.find_elements_by_tag_name('td')

        self.assertEqual(product_name.strip(), tds[1].text.strip())
        end_quantity = self.browser.find_element_by_class_name('boxshop-item-input').get_attribute('value')
        el = self.browser.find_element_by_class_name('basket-total')

        basket_total_pattern = 'Total\s+\$(\d+.\d+)'
        m = re.search(basket_total_pattern,el.text)
        basket_total = m.group(1)
        self.assertEqual(total, float(basket_total))

    def tearDown(self):
        self.browser.quit()


'''
US-3
'''
class TestRemoveFromCart(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.browser = webdriver.Chrome(executable_path='%s' % os.path.join(dir_path, 'chromedriver.exe'))
        self.browser.get(url)

    def test_remove_product_from_cart(self):
        product_name = self.browser.find_elements_by_class_name('boxshop-item-title')[0].text
        quantity = 23

        self.browser.find_element_by_class_name('boxshop-item-input').send_keys(Keys.BACKSPACE + str(quantity) + Keys.TAB)
        self.browser.find_element_by_class_name('boxshop-item-add').click()
        time.sleep(5)
        self.browser.find_element_by_class_name('basket-toggle').click()
        basket_count = int(self.browser.find_element_by_class_name('basket-count').text)

        self.assertEqual(quantity, basket_count)

        self.browser.find_element_by_class_name('basket-remove').click()

        time.sleep(3)

        try:
            self.browser.find_element_by_class_name('basket-count').text
        except Exception as e:
            pass


    def tearDown(self):
        self.browser.quit()


'''
US-4
'''
class TestCheckout(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.browser = webdriver.Chrome(executable_path='%s' % os.path.join(dir_path, 'chromedriver.exe'))
        self.browser.get(url)

    def test_checkout(self):
        checkout_url = 'https://m.kss.com.au/boxshop/checkout/step1'
        quantity = 23

        self.browser.find_element_by_class_name('boxshop-item-input').send_keys(Keys.BACKSPACE + str(quantity) + Keys.TAB)
        self.browser.find_element_by_class_name('boxshop-item-add').click()
        time.sleep(5)
        self.browser.find_element_by_class_name('basket-toggle').click()
        time.sleep(1)
        self.browser.find_element_by_xpath('//*[@id="basket-contents"]/div/table/tbody/tr[2]/td[3]/button').click()
        self.assertEqual(checkout_url, self.browser.current_url)

    def tearDown(self):
        self.browser.quit()


if __name__ == '__main__':
    suites = [unittest.TestLoader().loadTestsFromTestCase(TestModifyQuantity),
              unittest.TestLoader().loadTestsFromTestCase(TestAddToCart),
              unittest.TestLoader().loadTestsFromTestCase(TestRemoveFromCart),
              unittest.TestLoader().loadTestsFromTestCase(TestCheckout)
              ]
    for suite in suites:
        unittest.TextTestRunner(verbosity=2).run(suite)
