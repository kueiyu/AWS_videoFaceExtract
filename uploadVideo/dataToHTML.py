def htmlTableBody(metadata, video_path, img_path):
    with open('HTML/snippets/video.htm') as f:
        video_snippet = f.read()

    with open('HTML/snippets/face.htm') as f:
        face_snippet = f.read()

    table_body = ''
    for video in metadata:
        table_body += '<tr>'
        table_body += '<td>{}</td>'.format(video['video_filename'])
        table_body += '<td>' + video_snippet.format(video_path + video['video_filename']) + '</td>'
        table_body += '<td>{}</td>'.format(video['uploadDate'])
        table_body += '<td>{}</td>'.format(video['processTime'])
        table_body += '<td><table>'
        
        face_ages = video['face_ages'].split(',') # face ages stored in db as a single string separated by comma
        face_ages2 = video['face_ages2'].split(',')
        
        for i, face in enumerate(video['face_filenames']):
            try:
                age = face_ages[i]
            except:
                age = 'age unavailable'
            try:
                age2 = face_ages2[i]
            except:
                age2 = ''
            
            table_body += face_snippet.format(img_path + face, age, age2)
            
        table_body += '</table></td>'
        table_body += '</tr>'
    return table_body