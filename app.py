	
#app.py
from errno import EIDRM
from turtle import width
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from PIL import Image # Import Image class from the library.
from PIL import ImageEnhance
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['FILE_NAME'] = ''
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')

#method to upload image
def upload_logic():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
        
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        app.config['FILE_NAME'] = filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)   

#method to flip image horizontally
def horizontal():
    if app.config['FILE_NAME'] == '':
            flash('No file uploaded yet')
            return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        new_image = image.transpose(method=Image.FLIP_LEFT_RIGHT)
        new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', filename=filename)

#method to flip image vertically
def vertical():
    if app.config['FILE_NAME'] == '':
            flash('No file uploaded yet')
            return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        new_image = image.transpose(method=Image.FLIP_TOP_BOTTOM)
        new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', filename=filename)

#method to rotate image by degree
def rotate(degree):
    if app.config['FILE_NAME'] == '':
            flash('No file uploaded yet')
            return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        rotated_image = image.rotate(degree) # Rotate the image by 180 degrees.
        rotated_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', filename=filename)

#method to convert image into fixed and user specified grayscale
def Greyscale(value = 'L'):
    if app.config['FILE_NAME'] == '':
            flash('No file uploaded yet')
            return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        new_image = image.convert(value)
        new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', filename=filename)

#method to saturate/desaturate an image
def Saturate(saturation_factor):
    if app.config['FILE_NAME'] == '':
            flash('No file uploaded yet')
            return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        if saturation_factor >1:
            enhancer = ImageEnhance.Color(image)
        else:
            enhancer = ImageEnhance.Brightness(image)
        new_image = enhancer.enhance(saturation_factor)
        new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', filename=filename)

#method to resize an image by user specified x and y values
def Resize(x, y):
    if app.config['FILE_NAME'] == '':
            flash('No file uploaded yet')
            return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        new_image = image.resize((x, y))
        new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', filename=filename)

#method to resize an image by user specified percentage
def Resize_percent(percentage):
    if app.config['FILE_NAME'] == '':
            flash('No file uploaded yet')
            return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        width, height = image.size
        width = (width*percentage)//100
        height = (height*percentage)//100
        new_image = image.resize((width, height))
        new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', filename=filename)

#method to create thumbnail of an image
def Thumbnail():
    if app.config['FILE_NAME'] == '':
            #flash('No file uploaded yet')
            return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        size = 128, 128
        image.thumbnail(size)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', filename=filename)

#API endpoint for POST request
@app.route('/', methods=['GET','POST'])
def upload_image(): 
    if request.form['submit_button'] == 'Upload':  
        #flash("Uploading!") 
        return upload_logic()
    else:
        #flash("Transforming!")
        checkbox_array = request.form.getlist('operation')
        checkbox_length = len(checkbox_array)
        if checkbox_length == 0:
            flash("No Operation selected!")
        else:
            filename = app.config['FILE_NAME']
            for id in checkbox_array:
                if id == 'horizontal':
                    #flash("Horizonatal")
                    horizontal()
                if id == 'vertical':
                    #flash("Vertical")
                    vertical()
                if id == 'rotate':
                    #flash("Rotate")
                    degree = int(request.form['rotate_degree'])
                    #flash(degree)
                    rotate(degree)
                if id == 'grayscale':
                    #flash("Fixed greyscale")
                    Greyscale()
                if id == 'grayscale_factor':
                    #flash("Specified greyscale")
                    gray_val = request.form['grayscale_value']
                    Greyscale(gray_val)
                if id == 'saturate':
                    #flash("Saturate")
                    Saturate(5)
                if id == 'desaturate':
                    #flash("Desaturate")
                    Saturate(0.5)
                if id == 'resize_xy':
                    x = int(request.form['resize_x'])
                    y = int(request.form['resize_y'])
                    #flash("Resize" + str(x) + "," + str(y))
                    Resize(x,y)
                if id == 'resize_percent':
                    percentage = int(request.form['resize_percentage'])
                    #flash('resize by percentage' + ' ' + str(percentage))
                    Resize_percent(percentage)
                if id == 'thumbnail':
                    #flash("Thumbnail")
                    Thumbnail()
                if id == 'rotate_left':
                    #flash("Rotate Left")
                    rotate(90)
                if id == 'rotate_right':
                    #flash("Rotate Right")
                    rotate(-90)


        return render_template('index.html', filename=filename)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
 
if __name__ == "__main__":
    app.run()