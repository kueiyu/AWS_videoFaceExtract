def htmlTableBody(metadata, video_path, img_path):
    with open('HTML/snippets/video.htm') as f:
        video_snippet = f.read()

    with open('HTML/snippets/face.htm') as f:
        face_snippet = f.read()

    table_body = ''
    for video in metadata:
        table_body += '<tr>'
        table_body += '<td>' + video['video_filename'] + '</td>'
        table_body += '<td>' + video_snippet.replace('target', video_path + video['video_filename']) + '</td>'
        table_body += '<td>' + video['uploadDate'] + '</td>'
        table_body += '<td>' + video['processDate'] + '</td>'
        table_body += '<td><table>'
        for face in video['faces']:
            table_body += face_snippet.replace('target', img_path + face)
            # Add age here
        table_body += '</table></td>'
        table_body += '</tr>'
    return table_body