'''
Author : Murat Konuralp Şenoğlu / 171101009
Sherlock Project with Google ML Kit for Bil 481
'''

from google.cloud import vision


class ImageAnalyzer:

    asterix_length = 10     # asterix length for printing

    @classmethod
    def __concatLine(cls, string):
        return string + "\n"

    @classmethod
    def __detect_web_entities(cls, url):
        # Detects web annotations in the url and returns results as string.

        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = url

        web_detection_params = vision.types.WebDetectionParams(
            include_geo_results=True)
        image_context = vision.types.ImageContext(
            web_detection_params=web_detection_params)

        response = client.web_detection(image=image, image_context=image_context)
        annotations = response.web_detection
        asterixes = "*" * ImageAnalyzer.asterix_length
        prefix = asterixes + " Start of Web Entities results " + asterixes + "\n"
        postfix = asterixes + " End of Web Entities results " + asterixes + "\n"
        string = ""
        if annotations.best_guess_labels:
            for label in annotations.best_guess_labels:
                string += cls.__concatLine(('\nBest guess label: {}'.format(label.label)))

        if annotations.pages_with_matching_images:
            string += cls.__concatLine('\n{} Pages with matching images found:'.format(
                len(annotations.pages_with_matching_images)))

            for page in annotations.pages_with_matching_images:
                string += cls.__concatLine('\n\tPage url   : {}'.format(page.url))

                if page.full_matching_images:
                    string += cls.__concatLine('\t{} Full Matches found: '.format(
                        len(page.full_matching_images)))

                    for image in page.full_matching_images:
                        string += cls.__concatLine('\t\tImage url  : {}'.format(image.url))

                if page.partial_matching_images:
                    string += cls.__concatLine('\t{} Partial Matches found: '.format(
                        len(page.partial_matching_images)))

                    for image in page.partial_matching_images:
                        string += cls.__concatLine('\t\tImage url  : {}'.format(image.url))

        if annotations.web_entities:
            string += cls.__concatLine('\n{} Web entities found: '.format(
                len(annotations.web_entities)))

            for entity in annotations.web_entities:
                string += cls.__concatLine('\n\tConfidence Percentage      : %' + str(round(entity.score * 100)))
                string += cls.__concatLine(u'\tDescription: ' + entity.description)

        if annotations.visually_similar_images:
            string += cls.__concatLine('\n{} visually similar images found:'.format(
                len(annotations.visually_similar_images)))

            for image in annotations.visually_similar_images:
                string += cls.__concatLine('\tImage url    : {}'.format(image.url))
        if len(string) == 0:
            string = cls.__concatLine("No web entities found.")
        return prefix + string + postfix

    @classmethod
    def __detect_labels(cls, url):
        # detects labels in url and returns results as string

        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = url

        response = client.label_detection(image=image)
        labels = response.label_annotations
        string = ""
        asterixes = "*" * ImageAnalyzer.asterix_length
        prefix = asterixes + " Start of Labels results " + asterixes + "\n"
        postfix = asterixes + " End of Labels results " + asterixes + "\n"
        if len(labels) > 0:
            string += cls.__concatLine("There are " + str(len(labels)) + " landmarks found in the image:")
        else:
            string += cls.__concatLine("There are no landmarks detected in the image.")
        for label in labels:
            string += cls.__concatLine(
                "Image contains " + label.description + " with confidence percentage %" + str(round(label.score * 100)))
        return prefix + string + postfix

    @classmethod
    def __detect_landmarks(cls, url):
        # detects landmarks in the url and returns as string

        from google.cloud import vision
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = url

        response = client.landmark_detection(image=image)  # get landmark detection response from client
        landmarks = response.landmark_annotations
        s = ""
        asterixes = "*" * ImageAnalyzer.asterix_length
        prefix = asterixes + " Start of Landmarks results " + asterixes + "\n"
        postfix = asterixes + " End of Landmarks results " + asterixes + "\n"
        if len(landmarks) > 0:
            s += cls.__concatLine("There are " + str(len(landmarks)) + " landmarks found in the image:")
        else:
            s += cls.__concatLine("There are no landmarks detected in the image.")
        for landmark in landmarks:
            s += cls.__concatLine(
                "Landmark: " + landmark.description + ", Confidence percentage: %" + str(round(landmark.score * 100)))
        return prefix + s + postfix

    @classmethod
    def __detect_faces(cls, url):
        # detects faces in the url and returns results as string

        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = url

        response = client.face_detection(image=image)  # get face detection response from client
        faces = response.face_annotations

        # Names of likelihood from google.cloud.vision.enums
        likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                           'LIKELY', 'VERY_LIKELY')
        string = ""
        asterixes = "*" * ImageAnalyzer.asterix_length
        prefix = asterixes + " Start of Faces results " + asterixes + "\n"
        postfix = asterixes + " End of Faces results " + asterixes + "\n"
        if len(faces) > 0:  # message to print when faces are found
            string += cls.__concatLine("There are " + str(len(faces)) + " faces found in the image,\n")
        else:
            string += cls.__concatLine("There are no faces detected in the image.")
        for face in faces:  # add each face to the return string
            string += cls.__concatLine('anger: {}'.format(likelihood_name[face.anger_likelihood]))
            string += cls.__concatLine('joy: {}'.format(likelihood_name[face.joy_likelihood]))
            string += cls.__concatLine('sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))
            string += cls.__concatLine('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
            string += cls.__concatLine('headwear: {}'.format(likelihood_name[face.headwear_likelihood]))
            vertices = (['({},{})'.format(vertex.x, vertex.y)
                         for vertex in face.bounding_poly.vertices])
            string += cls.__concatLine('face bounds: {}'.format(','.join(vertices)))
            string += cls.__concatLine("")
        return prefix + string + postfix

    @classmethod
    def analyze_from_url(cls, url, search_in_web_entities, search_in_faces, search_in_labels, search_in_landmarks):
        # Calls respective analysis methods according to the boolean parameters and appends the return strings to an array if requested

        arr = []
        if search_in_web_entities:
            arr.append(cls.__detect_web_entities(url))
        if search_in_faces:
            arr.append(cls.__detect_faces(url))
        if search_in_labels:
            arr.append(cls.__detect_labels(url))
        if search_in_landmarks:
            arr.append(cls.__detect_landmarks(url))
        return arr

    @classmethod
    def analyze_and_print_from_url(cls, url, search_in_web_entities, search_in_faces, search_in_labels, search_in_landmarks):
        # Analyzes and prints according to respective boolean parameters
        analyses = cls.analyze_from_url(url, search_in_web_entities, search_in_faces, search_in_labels, search_in_landmarks)
        for analysis in analyses:
            print(analysis)
