from __future__ import print_function  # Only needed for Python 2
import json
from selenium_driver import seleniumChromeDriver
from selenium.webdriver.common.action_chains import ActionChains
import getpass
import time


class typeformCreator():

    def __init__(self, driver):
        """
        """
        self.driver = driver

    def login(self):
        """
        """
        self.driver.get('https://admin.typeform.com/login/')
        username = 'lpmayos@gmail.com'  # raw_input('Enter Typeform username: ')
        self.driver.send_keys('_username', username)
        password = 'vasdelpal4Um'  # getpass.getpass()
        self.driver.send_keys('_password', password)
        self.driver.click_element_by_id('btnlogin')

    def add_new_form(self):
        """
        """
        self.driver.click_element_by_css_selector('#forms .item.add div.label')  # 'Get started'
        time.sleep(5)
        self.driver.click_element_by_css_selector('.item.add .content .upper span')
        self.driver.send_keys('quickyform_name', 'form_prova')
        self.driver.click_element_by_id('submit-scratch-form')

    def add_text_to_tinymce(self, tinymce_id, text):
        """
        """
        # switch context to iframe
        self.driver.switch_to_frame(tinymce_id)
        self.driver.send_keys('tinymce', text)

        # switch back to parent form
        self.driver.driver.switch_to_default_content()


    def add_text_field(self, text):
        """
        """
        # add text field
        self.driver.click_element_by_css_selector('#sidebar .field-icon.statement')

        self.add_text_to_tinymce('statement_content_ifr', text)

    def add_video_field(self, url):
        """
        """
        video_on_off_element = self.driver.find_element_by_css_selector('#attachment .wrapper.coolCheckbox')
        if video_on_off_element.get_attribute("data-qa") == 'false':
            self.driver.click_element_by_css_selector('#attachment .front')  # Image / Video ON
        time.sleep(3)
        self.driver.click_element_by_css_selector('.attachment .video')  # select video tab

        self.driver.send_keys('statement_video_url', url)

    def add_text_with_video(self, video_url, start_time, end_time):
        """
        """
        text = 'Video ' + video_url + '. Please watch segment ' + str(start_time) + ' to ' + str(end_time) + ' and answer the questions below'
        self.add_text_field(text)

        # youtube_video_id = video_url.split('=')[1]
        # nice_url = 'https://www.youtube.com/v/' + youtube_video_id + '?start=' + str(int(start_time * 60)) + '&end=' + str(int(end_time * 60)) + '&version=3'
        nice_url = video_url + '&start=' + str(int(start_time * 60))
        self.add_video_field(nice_url)

        self.driver.click_element_by_css_selector('.submit span')

    def add_group(self, text):
        """
        """
        # add group of questions for a video
        self.driver.click_element_by_css_selector('#sidebar .field-icon.group')

        self.add_text_to_tinymce('group_content_ifr', text)

        self.driver.click_element_by_css_selector('.submit span')

    def add_opinion_scale_to_last_group(self, text, low_val_text, high_val_text):
        """
        """
        source_element = self.driver.find_element_by_css_selector('#sidebar .field-icon.opinion-scale')
        # dest_element = self.driver.driver.find_elements_by_css_selector('.field.group .fake-droppable.minidrag')[-1]
        dest_element = self.driver.driver.find_element_by_css_selector('.last-group .fake-droppable')
        action = ActionChains(self.driver.driver).drag_and_drop(source_element, dest_element)
        time.sleep(5)
        action.perform()

        # add title
        self.add_text_to_tinymce('opinion_scale_question_ifr', text)

        # add low and high values
        self.driver.send_keys('opinion_scale_negativeLabel', low_val_text)
        self.driver.send_keys('opinion_scale_positiveLabel', high_val_text)

        # make it required
        required_on_off_element = self.driver.driver.find_elements_by_css_selector('.wrapper.coolCheckbox')[2]
        if required_on_off_element.get_attribute("data-qa") == 'false':
            on_off = self.driver.driver.find_elements_by_css_selector('.wrapper.coolCheckbox .front')[2]  # Required ON
            on_off.click()

        self.driver.click_element_by_css_selector('.submit span')

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


def create_form_with_data(typeform_creator, data, video_ids):
    """
    """

    print('login....')
    typeform_creator.login()
    print('login done!')

    print('adding new form....')
    typeform_creator.add_new_form()
    print('new form added')

    for video_id in data.keys()[0:3]:
        video_data = data[video_id]
        video_url = video_data['url']  # https://www.youtube.com/v/qCVmntRBg8A?start=40&end=45&version=3
        start_time = video_data['start time']
        end_time = video_data['end time']
        captions = video_data['captions']
        print('adding video...')
        typeform_creator.add_video(video_url, start_time, end_time, captions)
        print('video added!')
    return


def main():
    """
    """
    # experiments = {'exp3': '/home/lpmayos/code/caption-guided-saliency/experiments/msr-vtt-experiment3/model-99.json',
    #                'exp4': '/home/lpmayos/code/caption-guided-saliency/experiments/msr-vtt-experiment4/model-99.json',
    #                'exp5': '/home/lpmayos/code/caption-guided-saliency/experiments/msr-vtt-experiment5/model-99.json'}
    # data = extract_data(experiments)
    # video_ids = ['video' + str(i) for i in range(7010, 7015)]

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
                   'captions': {'exp5': u'caption 2', 'exp4': u'caption 4'}}
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

    # driver = seleniumChromeDriver('/home/lpmayos/code/chromedriver')
    driver = seleniumChromeDriver('/Users/lpmayos/code/chromedriver')
    typeform_creator = typeformCreator(driver)
    create_form_with_data(typeform_creator, data, video_ids)


if __name__ == "__main__":
    main()
