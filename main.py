# Solution to Jane Street puzzle from December 2022
import numpy as np

display_position = False
display_move = False
display_invalid_move = False
display_cell_move = False
display_top_face = False
display_walk = False

# Puzzle grid. Start at 0,0; end at 6,6; x,y is row x, column y.
puzzle_grid = [[0,77,32,403,337,452],
[5,23,-4,592,445,620],
[-7,2,357,452,317,395],
[186,42,195,704,452,228],
[81,123,240,443,353,508],
[57,33,132,268,492,732]]

moves = ["up", "down", "left", "right"]
# Permutation arrays
up_perm = [3,0,1,2,4,5]
down_perm = [1,2,3,0,4,5]
left_perm = [5,1,4,3,0,2]
right_perm = [4,1,5,3,2,0]

count = 0


# cube_faces is a dictionary with 6 keys a,b,c,d,e,f and corresponding values displayed on the face of the key.
# Viewing the cube at 0,0, the labelling is as follows:
# a: top; b: front (towards row 1); c: bottom; d: back (towards row -1); e: left; f: right
#
# position: current position on the board (dictionary); N: number of move
# current faces: labelling of faces at current position (in array form)
# walk: moves so far
# walk_positions: dictionary of cells encountered so far
def perform_walk(cube_faces, position, N, score, current_faces, walk, walk_positions):
  global count
  #top_face_value = cube_faces.get(current_faces[0]) # Could be None
  if display_position:
    print(str(N) + ","+ str(score)+ ":" + str(position["row"]) + "," + str(position["col"]) + "|" + str(current_faces))
    print(cube_faces)
  if display_walk:
    print(walk)
  if position == {"row": 5, "col": 5}: # Reached end of board
    print("Found walk")
    count += 1
    #print(str(N) + ","+ str(score)+ ":" + str(position["row"]) + "," + str(position["col"]) + "|" + str(current_faces))
    print("Cube faces: " + str(cube_faces))
    #print(walk)
    print("Walk:")
    for position in walk_positions.items():
      print(position)
    result = 0
    print("Untouched cells:")
    for i in range(6):
      for j in range(6):
        if {"row": i, "col": j} in walk_positions.values():
          continue;
        else:
          print(str(i) + "," + str(j))
          result += puzzle_grid[i][j]
    print("Result: " + str(result))
    return
  for move in moves:
    if is_valid_move(move, position):
      new_position = find_position(move, position)
      new_row = new_position["row"]
      new_col = new_position["col"]
      new_index = new_row*6 + new_col
      cell_value = puzzle_grid[new_row][new_col]
      if display_cell_move:
        print(str(new_position) + "|" + str(cell_value))
      new_faces = update_current_faces(current_faces, move)

      # Face value of cube AFTER the move
      top_face_value = cube_faces.get(new_faces[0])
      if top_face_value == None:
        # Cube face has not been assigned yet, set a value to try
        new_face = (cell_value - score)/N
        #print("new_face: "+str(new_face))
        int_new_face = int(new_face)
        #print(int_new_face*N == cell_value - score)
        if int_new_face*N != cell_value - score: # not divisible by N, i.e. invalid move
          continue
        else:
          # Assign new value and continue the walk
          new_score = cell_value
          cube_faces.update({new_faces[0]: new_face})
          if display_top_face:
            print("Top face after move: " + str(top_face_value))
          if display_move:
            print(str(move) + " new")
          walk.update({N: move})
          walk_positions.update({N: {"row": new_row, "col": new_col}})
          perform_walk(cube_faces, new_position, N+1, new_score, new_faces, walk, walk_positions)
          # Remove assigned cube face value and continue
          cube_faces.pop(new_faces[0])
          walk_positions.pop(N)
          walk.pop(N)
          continue
      # End unassigned top face case

      else:
        # Cube face has been assigned, just need to check valid move
        new_faces = update_current_faces(current_faces, move)

        # Face value of cube AFTER the move
        top_face_value = cube_faces.get(new_faces[0])

        new_score = N*top_face_value + score

        if new_score == cell_value:
          # Passes the test, continue the walk
          new_faces = update_current_faces(current_faces, move)
          if display_top_face:
            print("Top face after move: " + str(top_face_value))
          if display_move:
            print(move)
          walk.update({N: move})
          walk_positions.update({N: {"row": new_row, "col": new_col}})
          perform_walk(cube_faces, new_position, N+1, new_score, new_faces, walk, walk_positions)
          # Backtrack and continue
          walk_positions.pop(N)
          walk.pop(N)
        else:
          # Fails, continue searching moves
          continue
      # End assigned top face case
    else:
      if display_invalid_move:
        print("Invalid move")
    # End valid move case
  # End for loop
  
# Checks whether a move is allowed (by the grid)
def is_valid_move(move, position):
  if move == "up":
    if position["row"] == 5:
      return False
    else:
      return True
  elif move == "down":
    if position["row"] == 0:
      return False
    else:
      return True
  elif move == "left":
    if position["col"] == 0:
      return False
    else:
      return True
  elif move == "right":
    if position["col"] == 5:
      return False
    else:
      return True
  else:
    return None

# Returns the position of the landing cell
def find_position(move, position):
  row = position["row"]
  col = position["col"]
  if move == "up":
    return {"row": row+1, "col": col}
  elif move == "down":
    return {"row": row-1, "col": col}
  elif move == "left":
    return {"row": row, "col": col-1}
  elif move == "right":
    return {"row": row, "col": col+1}
  else:
    return None

# Returns an array with the appropriate permutation of the faces, given a valid move and a current cube as input
def update_current_faces(current_faces, move):
  new_faces = [0,0,0,0,0,0] # Array of size 6
  if move == "up":
    permutation = up_perm
  elif move == "down":
    permutation = down_perm
  elif move == "left":
    permutation = left_perm
  elif move == "right":
    permutation = right_perm
  i=0
  for index in permutation:
    new_faces[i] = current_faces[index]
    i+=1
  return new_faces

perform_walk({}, {"row": 0, "col": 0}, 1, 0, ["a","b","c","d","e","f"], {}, {0:{"row": 0, "col": 0}})
print("Number of walks found: "+ str(count))
