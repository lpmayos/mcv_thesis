from __future__ import print_function  # Only needed for Python 2
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import getpass
import time


class typeformCreator():

    def __init__(self, driver, wait, username, password):
        """
        """
        self.driver = driver
        self.wait = wait
        self.username = username
        self.password = password

    def login(self):
        """
        """
        self.driver.get('https://admin.typeform.com/login/')
        element = self.driver.find_element_by_css_selector('#_username')
        element.send_keys(self.username)
        element = self.driver.find_element_by_css_selector('#_password')
        element.send_keys(self.password)
        self.driver.find_element_by_css_selector('#btnlogin').click()

    def add_new_form(self, num_form):
        """
        """
        self.driver.find_element_by_css_selector('#forms .item.add div.label').click()
        time.sleep(3)
        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.item.add .content .upper')))
        element.click()

        self.driver.find_element_by_css_selector('#quickyform_name').send_keys('mcv_eval_' + str(num_form))

        self.driver.find_element_by_css_selector('#submit-scratch-form').click()

    def add_text_to_tinymce(self, tinymce_id, text):
        """
        """
        # switch context to iframe
        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#' + tinymce_id)))
        self.driver.switch_to_frame(tinymce_id)
        element = self.driver.find_element_by_css_selector('#tinymce')
        element.send_keys(text)

        # switch back to parent form
        self.driver.switch_to_default_content()

    def add_video_field(self, url):
        """
        """
        video_on_off_element = self.driver.find_element_by_css_selector('#attachment .wrapper.coolCheckbox')
        if video_on_off_element.get_attribute("data-qa") == 'false':
            self.driver.find_element_by_css_selector('#attachment .front').click()  # Image / Video ON
        time.sleep(3)
        self.driver.find_element_by_css_selector('.attachment .video').click()  # select video tab

        element = self.driver.find_element_by_css_selector('#statement_video_url')
        element.send_keys(url)

    def seconds_to_printable_time(self, seconds):
        """
        """
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    def add_text_with_video(self, video_url, start_time, end_time):
        """
        """
        text = 'Video ' + video_url + '. Please watch segment ' + self.seconds_to_printable_time(start_time) + ' to ' + self.seconds_to_printable_time(end_time) + ' and answer the questions below'

        # add text field
        time.sleep(3)
        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#sidebar .field-icon.statement')))
        element.click()

        self.add_text_to_tinymce('statement_content_ifr', text)

        # youtube_video_id = video_url.split('=')[1]
        # nice_url = 'https://www.youtube.com/v/' + youtube_video_id + '?start=' + str(int(start_time * 60)) + '&end=' + str(int(end_time * 60)) + '&version=3'
        nice_url = video_url + '&start=' + str(int(start_time * 60))
        self.add_video_field(nice_url)

        self.driver.find_element_by_css_selector('.submit span').click()

    def add_group(self, text):
        """
        """
        time.sleep(3)

        # add group of questions for a video
        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#sidebar .field-icon.group')))
        element.click()

        self.add_text_to_tinymce('group_content_ifr', text)

        self.driver.find_element_by_css_selector('.submit span').click()

    def add_opinion_scale_to_last_group(self, text, low_val_text, high_val_text):
        """
        """
        time.sleep(3)
        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#sidebar .field-icon.opinion-scale')))
        element.click()

        # add title
        self.add_text_to_tinymce('opinion_scale_question_ifr', text)

        # add low and high values
        element = self.driver.find_element_by_css_selector('#opinion_scale_negativeLabel')
        element.send_keys(low_val_text)
        element = self.driver.find_element_by_css_selector('#opinion_scale_positiveLabel')
        element.send_keys(high_val_text)

        # make it required
        required_on_off_element = self.driver.find_elements_by_css_selector('.wrapper.coolCheckbox')[-2]
        if required_on_off_element.get_attribute("data-qa") == 'false':
            on_off = self.driver.find_elements_by_css_selector('.wrapper.coolCheckbox .front')[-2]  # Required ON
            on_off.click()

        self.driver.find_element_by_css_selector('.submit span').click()

        # move to upper group
        time.sleep(3)
        aux = self.driver.find_elements_by_css_selector('.field.opinion-scale .action-move')[-1]
        action = ActionChains(self.driver).drag_and_drop_by_offset(aux, 0, -60)
        # time.sleep(3)
        action.perform()

    def add_caption(self, video_url, start_time, end_time, caption):
        """
        """
        text = 'Caption ' + caption
        self.add_group(text)
        self.add_opinion_scale_to_last_group('Coherence. Judge the logic and readability of the sentence.', 'Low', 'High')
        self.add_opinion_scale_to_last_group('Relevance. Judge if the sentence contains the more relevant and important objects/actions/events in the video clip', 'Low', 'High')
        self.add_opinion_scale_to_last_group('Helpful for blind. Judge how helpful would the sentence be for a blind person to understand what is happening in this video clip', 'Poor', 'Great')

    def add_video(self, video_url, start_time, end_time, captions):
        """
        """
        self.add_text_with_video(video_url, start_time, end_time)
        for caption in captions:
            self.add_caption(video_url, start_time, end_time, captions[caption])

    def add_welcome_screen(self):
        """
        """
        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#sidebar .field-icon.intro')))
        element.click()

        # add text
        title = 'Improving the quality of video-to-language models by an optimized annotation of the training material - Survey questionnaire'
        self.add_text_to_tinymce('intro_body_ifr', title)

        desc_on_off_element = self.driver.find_element_by_css_selector('#description .wrapper.coolCheckbox')
        if desc_on_off_element.get_attribute("data-qa") == 'false':
            self.driver.find_element_by_css_selector('#description .front').click()  # Description ON
        time.sleep(3)

        desc = 'Automatic video captioning is one of the ultimate challenges of Natural Language Processing, boosted by the omnipresence of video and the release of large-scale annotated video benchmarks. However, the specificity and quality of the captions vary considerably, having and adverse effect on the quality of the trained captioning models. In my master thesis I address this issue by propossing automatic strategies for optimizing the annotations of video material, removing annotations that are not semantically relevant and generating new and more informative captions.\n\nI need your help to evaluate my approach. Thanks for your collaboration :) It will take you no more than 10 minutes, I promise!'
        self.add_text_to_tinymce('intro_description_ifr', desc)

        self.driver.find_element_by_css_selector('.submit span').click()


def extract_data(experiments):
    """ Returns a data structure containing the generated captions for the indicated experiments. Example:
        data['video7015'] = {'id': 7015,
                             'category': 7,
                             'url': u'https://www.youtube.com/watch?v=rSYRh2ACa9Y',
                             'video_id': u'video7015',
                             'start time': 80.81,
                             'end time': 91.41,
                             'split': u'test',
                             'captions': {'exp5': u'a man and a woman are talking', 'exp4': u'a woman is talking to a man'}}
    """

    with open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/test_videodatainfo.json', 'r') as f:
        f_json = json.load(f)
        test_videos_info = f_json['videos']
    f.close()

    data = {}
    for i in range(7010, 10000):
        video_data = test_videos_info[i - 7010]  # i.e. {u'category': 10, u'url': u'https://www.youtube.com/watch?v=Sa4BUsvAcjc', u'video_id': u'video7010', u'start time': 401.51, u'end time': 419.65, u'split': u'test', u'id': 7010}
        video_data['captions'] = {exp: None for exp in experiments.keys()}
        data['video' + str(i)] = video_data

    for experiment in experiments:
        with open(experiments[experiment], 'r') as f:
            experiment_data = json.load(f)
            predictions = experiment_data['predictions']  # keys: 'video7010' - 'video9999'
            for video_id in predictions:
                caption = predictions[video_id][0]['caption']
                data[video_id]['captions'][experiment] = caption
    return data


def create_form_with_data(typeform_creator, data, video_ids, num_form):
    """
    """
    print('login....')
    try:
        typeform_creator.login()
    except NoSuchElementException:
        print('login was already done')
    print('login done!')

    print('adding new form....')
    typeform_creator.add_new_form(num_form)
    print('new form added')

    typeform_creator.add_welcome_screen()

    for video_id in video_ids:
        video_data = data[video_id]
        video_url = video_data['url']  # https://www.youtube.com/v/qCVmntRBg8A?start=40&end=45&version=3
        start_time = video_data['start time']
        end_time = video_data['end time']
        captions = video_data['captions']
        print('adding video...')
        typeform_creator.add_video(video_url, start_time, end_time, captions)
        print('video added!')
    return


def create_demo_form(typeform_creator):
    """
    """
    data = {}
    video1_data = {'id': 1,
                   'category': 7,
                   'url': u'https://www.youtube.com/watch?v=rSYRh2ACa9Y',
                   'video_id': u'video1',
                   'start time': 10.81,
                   'end time': 10.41,
                   'split': u'test',
                   'captions': {'exp5': u'caption 1', 'exp4': u'caption 2'}}
    video2_data = {'id': 2,
                   'category': 8,
                   'url': u'https://www.youtube.com/watch?v=rSYRh2ACa9Y',
                   'video_id': u'video2',
                   'start time': 20.81,
                   'end time': 20.41,
                   'split': u'test',
                   'captions': {'exp5': u'caption 3', 'exp4': u'caption 4'}}
    video3_data = {'id': 3,
                   'category': 9,
                   'url': u'https://www.youtube.com/watch?v=rSYRh2ACa9Y',
                   'video_id': u'video3',
                   'start time': 30.81,
                   'end time': 30.41,
                   'split': u'test',
                   'captions': {'exp5': u'caption 5', 'exp4': u'caption 6'}}
    data['video1'] = video1_data
    data['video2'] = video2_data
    data['video3'] = video3_data
    video_ids = ['video1', 'video2', 'video3']

    num_form = 1
    create_form_with_data(typeform_creator, data, video_ids, num_form)


def create_forms(typeform_creator):
    """
    """
    experiments = {'exp3': '/home/lpmayos/code/caption-guided-saliency/experiments/msr-vtt-experiment3/model-99.json',
                   'exp4': '/home/lpmayos/code/caption-guided-saliency/experiments/msr-vtt-experiment4/model-99.json',
                   'exp5': '/home/lpmayos/code/caption-guided-saliency/experiments/msr-vtt-experiment5/model-99.json'}
    data = extract_data(experiments)

    forms = [['video7010', 'video7011', 'video7012', 'video7013'],
             ['video7020', 'video7021', 'video7022', 'video7023']]

    for i, video_ids in enumerate(forms):
        create_form_with_data(typeform_creator, data, video_ids, i)


def main():

    # ask typeform username and password
    username = raw_input('Enter Typeform username: ')
    password = getpass.getpass()

    try:
        driver = webdriver.Chrome('/Users/lpmayos/code/chromedriver')  # osx
    except:
        driver = webdriver.Chrome('/home/lpmayos/code/chromedriver')  # ubuntu

    # driver = webdriver.Firefox(executable_path='/home/lpmayos/code/geckodriver')  # ubuntu

    wait = WebDriverWait(driver, 10)

    typeform_creator = typeformCreator(driver, wait, username, password)

    # # demo
    # create_demo_form(typeform_creator)

    # create forms
    create_forms(typeform_creator)


if __name__ == "__main__":
    main()