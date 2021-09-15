"""
    I don't know in the selenium if you can locate the element found within other html tag lets say you have the <a> tag
    located inside <legend> tag  and <p> tag like the following pattern

    <legend>
        <p>
            <a href="#">Click here </a>
        </p>
    </legend>


    for that case what if I want to locate the element of link 'click here' from the parent <p> and <legend>
    In selenium I don't see this way but I think there is a way to do so......
    But in the BeautifulSoup you can use the selector passed to the select() method like the following


    import bs4 
    exampleFile = open('example.html')
    exampleSoup = bs4.BeautifulSoup(exampleFile.read())
    elementOfLink = exampleSoup.select('legend > p > a')  # This means all the source codes of this <a> element on this files is dragged and stored inside the list for you to iterate their result 

    ## This is how we do in BeautifulSoup, I don't know how to achieve this in Selenium, but I try to figuring out 
    ## and wait for me I will come with the solution, Don't worry this IS AUTOMATION IS ABOUT!!!! KEEP IT UP PASCHAL....LETS MAKE IT




    Let's me Guess how to emplement above scenario using the selenium.........

    from selenium import webdriver
    browser = webdriver.Firefox()
    browser.get('http://127.0.0.1:8000/')

    # Then here from the browser we find the element with the given name, id, class etc
    # This element we get after finding it we store it inside the 'WebElement' object, I think from this object
    # you can get what you want through calling its associated methods and attributes(see them on page 258 of your book)
    # like the  following, 
    # One of interesting method of webelement object is 'location' where it returns the a dictionary with x and y for the 
    # position  of the element in the page
    # lets continue our code from above

    try:
        elem = browser.find_element_by_class_name('bookcover')
        print('Found <%s> element with that class name! % (elem.tag_name))   # this tag_name attr return the tag associated by the element like <img>, <div> etc
    except:
        print('Was not  be able to find an element with that name.')



    # lets come to this for my first case of finding the element of <a> which is inside <p> and <legend>

    try:
        legendElem = browser.find_element_by_class_name('legend')
        pElem = legendElem.find_element_by_class_name('p')
        aElem = pElem.find_element_by_class_name('a')
    else:
        print('You are wrong bro! there is no way for your scenario')


    # For our Fua Yako browser the full path to get the login/signup button is 
    <header><div><div><div><a>
    # YEESSSSS!!!! I GOT THE SOLUTION, FOR THAT CASE FOR COMPLEX PATH WE USE THE 'find_element(s)_by_xpath()'
    # You should read a book of 'Python Selenium Binding' there is Absolute and relative path everyone has its adv and disadv
    # lets read your book 'Python Selenium Binding' to understand it more.... But for now I'm going to implement it

"""





"""
GMAIL XPATH 
fname >>>>> id == 'firstName'
lname >>>>> id == 'lastName'
username >>>> id == 'username'  # this is the username field where its appended @gmail.com by default
password1 >>>> xpath = "//div[@id='passwd']/div/div/div[@class='Xb9hP']/input[@name='Passwd']"
password2 >>>> xpath = "//div[@id='confirm-passwd']/div/div/div[@class='Xb9hP']/input[@name='ConfirmPasswd']"

"""
from selenium import webdriver
browser = webdriver.Firefox()
import time
import pyautogui
browser.get('http://127.0.0.1:8000/')

browser.maximize_window()  # this is function for maximizing window since by default the window is minimized
print(browser.current_window_handle)
time.sleep(2)
try:
    signUpElem = browser.find_element_by_xpath("//header/div/div/div[2]/a")  # this is use to get the link for signUp
    signUpElem.click()
    print(browser.current_window_handle)
    time.sleep(3)
    #newURL = browser.window_handles[0]
    #browser.switch_to.window(newURL)
    laundrySignUpElem = browser.find_element_by_xpath("//section[@id='team']/div/div/div[2]/div/div/a")   
    #laundrySignUpElem = browser.find_element_by_id('filler')  
    laundrySignUpElem.click()
    time.sleep(3)

    fnameElem = browser.find_element_by_xpath("//input[@id='id_first_name']")
    fnameElem.click()
    fnameElem.send_keys('Yost')
    time.sleep(2)
    lnameElem = browser.find_element_by_xpath("//input[@id = 'id_last_name']")
    lnameElem.click()
    lnameElem.send_keys('Kalone')
    time.sleep(2)
    emailElem = browser.find_element_by_xpath("//input[@id='id_email']")
    emailElem.click()
    emailElem.send_keys('sost@test.com')
    time.sleep(2)
    pass1Elem = browser.find_element_by_xpath("//input[@id='id_password1']")
    pass1Elem.click()
    pass1Elem.send_keys('paschal123')
    time.sleep(2)
    pass2Elem = browser.find_element_by_xpath("//input[@id='id_password2']")
    pass2Elem.click()
    pass2Elem.send_keys('paschal123')
    time.sleep(2)
    pass2Elem.submit()

    time.sleep(5)
    mobileElem = browser.find_element_by_xpath("//div[@id='div_id_tele']/div/input[@id='id_tele']")
    mobileElem.click()
    mobileElem.send_keys("0782848498")
    regionElem = browser.find_element_by_xpath("//input[@id='id_region']")
    regionElem.click()
    regionElem.send_keys('Dar es salaam')
    districtElem = browser.find_element_by_xpath("//input[@id='id_district']")
    districtElem.send_keys('Ilala')
    wardElem = browser.find_element_by_xpath("//input[@id='id_ward']")
    wardElem.send_keys('Vingunguti')
    picElem = browser.find_element_by_xpath("//input[@id='id_photo']")
    #picElem.click()
    pyautogui.click(409, 406)
    time.sleep(5)
    pyautogui.click(286, 280)
    time.sleep(5)
    pyautogui.click(536, 252)
    time.sleep(5)
    pyautogui.click(1369, 45)
    time.sleep(2)

    streetElem = browser.find_element_by_xpath("//input[@id='id_street']")
    streetElem.send_keys('Kombo')
    locationElem = browser.find_element_by_xpath("//textarea[@id='id_location']")
    locationElem.send_keys("I'm living at Msalaban street near by the Kombo primary school for any information about me you can ask my famous name of Chausiku HandsomeBoy")
    accElem = browser.find_element_by_xpath("//input[@id='id_account_number']")
    accElem.click()
    accElem.send_keys('0867688723')
    locationElem.submit()
except:
    print("These elements have bad syntax")
