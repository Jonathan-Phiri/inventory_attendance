import qrcode
# Generate QR code for student
def generate_qr_code(student_id, student_name):
    data = {'student_id': student_id, 'student_name': student_name}
    img = qrcode.make(data)
    img.save(f'{student_id}.png')

generate_qr_code('2020004577', 'Chama Musonda')
