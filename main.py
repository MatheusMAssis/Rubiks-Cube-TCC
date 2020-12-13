### Importing libraries
from flask import Flask, jsonify, make_response, request,render_template
from flask_cors import CORS
from ida_star import to_linear_array, main, to_main_array
from cube import scramble, make_move
import numpy as np

app = Flask(__name__)
origins = ["*", "/*", "http://127.0.0.1:4200"]
solution_list = []
scrambled_list = []
actual_array = None

CORS(app, resources={ r'/*': {'origins': origins}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

def show_list_on_string(lst):
    result_string = ""
    for item in lst:
        result_string += item + " "
    return result_string

def map_initial_to_color(linear_arr):
    mapped_linear_arr = []
    map_dict = {'W': 'color1', 
                'G': 'color2', 
                'R': 'color3', 
                'B': 'color4', 
                'O': 'color5', 
                'Y': 'color6'}
    for initial in linear_arr:
        mapped_linear_arr.append(map_dict[initial])
    return np.array(mapped_linear_arr)
    
def set_initial_array():
    initial_array = np.array([
        ['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W'],
        ['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G'],
        ['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R'],
        ['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B'],
        ['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O'],
        ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']
    ])
    return initial_array

@app.route("/scrambled/solve", methods=["GET", "POST"])
def solve_cube():
    global actual_array, solution_list, scrambled_list

    if len(solution_list) >= 1:
        make_move(actual_array, solution_list.pop())
    else:
        solution_list = "Solucionado!"[-1::-1]

    state_array = map_initial_to_color(to_linear_array(actual_array))

    return render_template(
        "solution.html",

        #upper face
        c1=state_array[0], c2=state_array[1], c3=state_array[2],
        c4=state_array[3], c5=state_array[4], c6=state_array[5],
        c7=state_array[6], c8=state_array[7], c9=state_array[8],
        
        #left face
        c10=state_array[11], c11=state_array[10], c12=state_array[9],
        c13=state_array[23], c14=state_array[22], c15=state_array[21],
        c16=state_array[35], c17=state_array[34], c18=state_array[33],

        #front face
        c19=state_array[12], c20=state_array[13], c21=state_array[14],
        c22=state_array[24], c23=state_array[25], c24=state_array[26],
        c25=state_array[36], c26=state_array[37], c27=state_array[38],

        #right face
        c28=state_array[15], c29=state_array[16], c30=state_array[17],
        c31=state_array[27], c32=state_array[28], c33=state_array[29],
        c34=state_array[39], c35=state_array[40], c36=state_array[41],

        #back face
        c37=state_array[20], c38=state_array[19], c39=state_array[18],
        c40=state_array[32], c41=state_array[31], c42=state_array[30],
        c43=state_array[44], c44=state_array[43], c45=state_array[42],

        #lower face
        c46=state_array[51], c47=state_array[52], c48=state_array[53],
        c49=state_array[48], c50=state_array[49], c51=state_array[50],
        c52=state_array[45], c53=state_array[46], c54=state_array[47],

        scrambled_moves = show_list_on_string(scrambled_list),

        solution_moves = show_list_on_string(solution_list[-1::-1]),
    )

@app.route("/scrambled", methods=["GET", "POST"])
def scramble_cube():
    global actual_array, solution_list, scrambled_list

    new_initial_array = set_initial_array()
    scrambled_list = scramble(new_initial_array, 5)
    state_array = map_initial_to_color(to_linear_array(new_initial_array))

    solution_list = main(new_initial_array)
    actual_array = new_initial_array

    return render_template(
        "solution.html", 
        
        #upper face
        c1=state_array[0], c2=state_array[1], c3=state_array[2],
        c4=state_array[3], c5=state_array[4], c6=state_array[5],
        c7=state_array[6], c8=state_array[7], c9=state_array[8],
        
        #left face
        c10=state_array[11], c11=state_array[10], c12=state_array[9],
        c13=state_array[23], c14=state_array[22], c15=state_array[21],
        c16=state_array[35], c17=state_array[34], c18=state_array[33],

        #front face
        c19=state_array[12], c20=state_array[13], c21=state_array[14],
        c22=state_array[24], c23=state_array[25], c24=state_array[26],
        c25=state_array[36], c26=state_array[37], c27=state_array[38],

        #right face
        c28=state_array[15], c29=state_array[16], c30=state_array[17],
        c31=state_array[27], c32=state_array[28], c33=state_array[29],
        c34=state_array[39], c35=state_array[40], c36=state_array[41],

        #back face
        c37=state_array[20], c38=state_array[19], c39=state_array[18],
        c40=state_array[32], c41=state_array[31], c42=state_array[30],
        c43=state_array[44], c44=state_array[43], c45=state_array[42],

        #lower face
        c46=state_array[51], c47=state_array[52], c48=state_array[53],
        c49=state_array[48], c50=state_array[49], c51=state_array[50],
        c52=state_array[45], c53=state_array[46], c54=state_array[47],

        scrambled_moves = show_list_on_string(scrambled_list),

        solution_moves = show_list_on_string(solution_list[-1::-1]),
    )

@app.route("/", methods=["GET"])
def home():
    main_initial_array = set_initial_array()
    state_array = map_initial_to_color(to_linear_array(main_initial_array))

    print(main_initial_array)

    return render_template(
        "index.html", 
        
        #upper face
        c1=state_array[0], c2=state_array[1], c3=state_array[2],
        c4=state_array[3], c5=state_array[4], c6=state_array[5],
        c7=state_array[6], c8=state_array[7], c9=state_array[8],
        
        #left face
        c10=state_array[11], c11=state_array[10], c12=state_array[9],
        c13=state_array[23], c14=state_array[22], c15=state_array[21],
        c16=state_array[35], c17=state_array[34], c18=state_array[33],

        #front face
        c19=state_array[12], c20=state_array[13], c21=state_array[14],
        c22=state_array[24], c23=state_array[25], c24=state_array[26],
        c25=state_array[36], c26=state_array[37], c27=state_array[38],

        #right face
        c28=state_array[15], c29=state_array[16], c30=state_array[17],
        c31=state_array[27], c32=state_array[28], c33=state_array[29],
        c34=state_array[39], c35=state_array[40], c36=state_array[41],

        #back face
        c37=state_array[20], c38=state_array[19], c39=state_array[18],
        c40=state_array[32], c41=state_array[31], c42=state_array[30],
        c43=state_array[44], c44=state_array[43], c45=state_array[42],

        #lower face
        c46=state_array[51], c47=state_array[52], c48=state_array[53],
        c49=state_array[48], c50=state_array[49], c51=state_array[50],
        c52=state_array[45], c53=state_array[46], c54=state_array[47],
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0')
