from pyramid.response import Response
from pyramid.view import view_config

from pyramid.httpexceptions import HTTPFound, HTTPForbidden

from check_brenford import check_brenford

import os
import shutil


@view_config(
        route_name="home", 
        renderer="templates/home.jinja2"
)
def home_view(request):
    """
    Directs to home page when the request is GET,
    whereas if the request is POST, the file is uploade is the file extension is .csv
    """

    # For POST method
    if request.method == "POST":
        # Filename
        filename = request.POST['CSVfile'].filename

        # Checking if the file is of .csv format
        # If the file is of .csv format it gets uploaded
        if filename.split(".")[-1].lower() == "csv":
            file_data = request.POST["CSVfile"].file

            file_path = os.path.join('uploads', filename)

            with open(file_path, 'wb') as output_file:
                shutil.copyfileobj(file_data, output_file)

            # Process the csv file to check whether it follows Brenford law, and redirects to result page
            return HTTPFound(location=request.route_url("result", filename=filename))
        
        # If the file isnot of .csv format, it redirects to error page
        else:
            return HTTPFound(location=request.route_url("error", error_type="upload-error"))
    
    # For GET request, it sends an empty dictionary
    return {}

    

@view_config(
        route_name="result",
        renderer="json"
)
def result_view(request):
    """
    Result Page: it shows whether the given data follows Brenford Law
    If yes, return the calculated data: observed percentage, observed frequency, expected frequency and expected percentage
    """

    # Accessing hte file uploaded by user
    filename = request.matchdict['filename']

    # If the user decided to use api
    # NOTE: There is no premade api, so, presently it uses random distribution
    if filename == "random":
        brenford_proof, result = check_brenford(file=None, random_dist=True)
    else:
        file = os.path.join('uploads', filename)
        brenford_proof, result = check_brenford(file)

    # If Brenford Law proved, returns the calculated data
    if brenford_proof:
        return {
                "Success": True,
                "result": result
        }
    # Else redirects to the error page of not satisfying Brenford Law
    else:
        return HTTPFound(location=request.route_url("error", error_type="law-disproof"))


@view_config(
        route_name="error"
)
def file_upload_error_view(request):
    """
    This view is use to show different error messages.
    """
    error_msg = request.matchdict["error_type"]

    # If the user upload different file except the .csv file
    if error_msg == "upload-error":
        raise HTTPForbidden("File should be of CSV format")
    
    # Brenford law disapproved message
    elif error_msg == "law-disproof":
        return Response("<h3>The distribution doesnot follow Brenford Law.</h3>")