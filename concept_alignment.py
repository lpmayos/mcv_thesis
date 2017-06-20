class ConceptAlignment(object):

    def __init__(self, video_captions):
        """ returns a new VideoAnnotations object: a list of dictionaries containing
        the information of all the sentences captioning the video with id
        'video_id'. See samples/video_captions_sample.txt for an example.
        """
        for sentence1 in video_captions.sentences:
            for sentence2 in video_captions.sentences:
                min_distance = (None, float('inf'))
                for token1 in sentence1['tokens']:
                    for token2 in sentence2['tokens']:
                        distance = computeDistance(token1, token2)
                        if distance < min_distance(1):
                            min_distance = (token2, distance)

