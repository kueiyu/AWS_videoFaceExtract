import sys
from cv2 import VideoCapture, resize, imwrite
from face_recognition import face_locations, face_encodings, compare_faces, face_distance
from numpy import argmin


def extractFaces(media_path, filename, output_path):
    cap = VideoCapture(media_path + filename)
    print('Video loaded')

    extracted, face_areas, image_name = [], [], []
    process_this_frame = True
    num_of_captured = 0

    while True:
        try:
            ret, frame = cap.read()
            small_frame = resize(frame, (0, 0), fx=0.25, fy=0.25)
        except:
            break
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            locations = face_locations(rgb_small_frame, number_of_times_to_upsample=1)
            captured = face_encodings(rgb_small_frame, locations)
            for i, face in enumerate(captured):
                top, right, bottom, left = locations[i]
                area = (right-left)*(bottom-top)
                matches = compare_faces(extracted, face)
                if matches and any(matches):
                    face_distances = face_distance(extracted, face)
                    best = argmin(face_distances)
                    if matches[best] and area >= face_areas[best]:
                        extracted[best] = face
                        face_areas[best] = area
                        image_name[best] = filename + '_' + str(best + 1) + '.jpg'
                        imwrite(output_path + image_name[best], frame[top*4:bottom*4, left*4:right*4]) # Save only the face
                        #print('Existing face imgage overwrote')
                else:
                    extracted.append(face)
                    face_areas.append(area)
                    num_of_captured += 1
                    image_name.append(filename + '_' + str(num_of_captured) + '.jpg')
                    imwrite(output_path + image_name[-1], frame[top*4:bottom*4, left*4:right*4])  # Save only the face
                    print('New face imgage extracted')

        process_this_frame = not process_this_frame
    return image_name

if __name__ == '__main__':
    media_path, filename, output_path = sys.argv[1:4]   
    print(extractFaces(media_path, filename, output_path))