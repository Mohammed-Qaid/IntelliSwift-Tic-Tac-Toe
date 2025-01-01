import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        
        self.size_label = tk.Label(root, text="Enter grid size (3-10):")
        self.size_label.pack()
        
        self.size_entry = tk.Entry(root)
        self.size_entry.insert(0, "3")  # Default size is 3
        self.size_entry.pack()
        
        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.canvas = None
        self.board = []
        self.DEFENSE = []
        self.ATTACK = []

        # Start the game with a default size of 3
        self.start_game()

        self.reset_button = tk.Button(root, text="Reset Game", command=self.reset_game)
        self.reset_button.pack()

    def start_game(self):
        try:
            size = int(self.size_entry.get())
            if size < 3 or size > 10:
                raise ValueError("Size must be between 3 and 10.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        self.size = size
        self.board = [[" " for _ in range(self.size)] for _ in range(self.size)]
        self.DEFENSE = []
        self.ATTACK = []
        
        if self.canvas:
            self.canvas.destroy()
        
        self.canvas = tk.Canvas(self.root, width=100 * self.size, height=100 * self.size)
        self.canvas.pack()
        
        self.create_grid()
        self.canvas.bind("<Button-1>", self.make_move)
        
    # To draw the grid with size which the user select it.
    def create_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                self.canvas.create_rectangle(j * 100, i * 100, j * 100 + 100, i * 100 + 100, outline="black")

    # function to check the winner if founded.
    def check_winner(self):
        for row in self.board:
            if all(cell == row[0] != " " for cell in row):
                return row[0]
        
        for col in range(self.size):
            if all(self.board[row][col] == self.board[0][col] != " " for row in range(self.size)):
                return self.board[0][col]
        
        if all(self.board[i][i] == self.board[0][0] != " " for i in range(self.size)):
            return self.board[0][0]
        
        if all(self.board[i][self.size - 1 - i] == self.board[0][self.size - 1] != " " for i in range(self.size)):
            return self.board[0][self.size - 1]
        
        return None


    # Function to find all the possibilities from the empty cells that allow the player which in (i,j) to win the game.
    # Used for adding the possibilities for defense/attack lists.
    def get_available_cells(self, i, j, player_value):
        # player_value may be X, or O.
        empty_cells = []
        temp = []
        # to get the available cells in the same row.
        if all(self.board[i][col] in (" ", player_value) for col in range(self.size)):
            for col in range(self.size):
                if self.board[i][col] == " " and col !=j:
                    temp.append((i, col))
            empty_cells.append(temp)
            temp = []
        # to get the available cells in the same column.
        if all(self.board[row][j] in (" ", player_value) for row in range(self.size)):
            for row in range(self.size):
                if self.board[row][j] == " " and row !=i:
                    temp.append((row, j))
            empty_cells.append(temp)
            temp = []
        # to get the available cells in the main diagonal.
        if i == j:
            if all(self.board[d][d] in (" ", player_value) for d in range(self.size)):
                for d in range(self.size):
                    if self.board[d][d] == " " and not (i==d and j==d):
                        temp.append((d, d))
                empty_cells.append(temp)
                temp = []
        # to get the available cells in the inverse diag.
        if i + j == self.size - 1:
            if all(self.board[d][self.size - 1 - d] in (" ", player_value) for d in range(self.size)):
                for d in range(self.size):
                    if self.board[d][self.size - 1 - d] == " " and not (d==i and (self.size-1-d ==j)):
                        temp.append((d, self.size - 1 - d))
                empty_cells.append(temp)

        return empty_cells


    # Function to Update the defense list and attack list after the player or AI plays by removing the (i,j) position. 
    def remove_index_from_list(self, data, i, j, mode):
        # mode = 0: to remove only the index (i,j) from the defense/attack lists.
        # mode = 1: to remove all possibilities connected by the index (i,j).
        tuple_to_remove = (i, j)
        if mode == 0:
            for inner_list in data:
                if tuple_to_remove in inner_list:
                    if len(inner_list) > 1:
                        inner_list.remove(tuple_to_remove)
                    else:
                        data.remove(inner_list)
        elif mode == 1:
            data[:] = [inner_list for inner_list in data if tuple_to_remove not in inner_list]
    
    # This function is to determine the shared indices in the DEFENSE and ATTACK lists.
    def find_intersection(self):
        # Flatten the lists
        flat_a = {tuple(t) for sublist in self.ATTACK for t in sublist}
        flat_b = {tuple(t) for sublist in self.DEFENSE for t in sublist}

        # Find common tuples
        common_tuples = flat_a.intersection(flat_b)

        return list(common_tuples)

    # function to update the defense/attack lists at each move.
    def update_lists(self,row,col,player):
        if player=='X':
            # to remove the selected positions from defense list 
            # and remove the selected position with all conneced possibilities from attack list
            self.remove_index_from_list(self.DEFENSE, row, col, 0)
            self.remove_index_from_list(self.ATTACK, row, col, 1)
            
            # to add the available cells into defense list based on (row,col) index.
            a=self.get_available_cells(row, col, "X")
            for x in a:
                if x not in self.DEFENSE:
                    self.DEFENSE.append(x)
            self.DEFENSE = sorted(self.DEFENSE, key=len) # to sort from the smaller length to larger length
        else:
            # to remove the selected positions from attack list 
            # and remove the selected position with all conneced possibilities from defense list
            self.remove_index_from_list(self.DEFENSE, row, col, 1)
            self.remove_index_from_list(self.ATTACK, row, col, 0)
            a=self.get_available_cells(row, col, "O")
            for x in a:
                if x not in self.ATTACK:
                    self.ATTACK.append(x)
            self.ATTACK = sorted(self.ATTACK, key=len)

    # function to assign X for the player position.
    def player_move(self, row, col):

        if self.board[row][col] == " ":
            self.board[row][col] = "X"
            self.update_lists(row,col,"X")
            return True
        return False
    
    
    # function to assign O for the AI position which selected based on defense/attack lists.
    def ai_move(self):
        if len(self.ATTACK)==0 and len(self.DEFENSE)==0:
            arr = [[(i, j), self.get_available_cells(i, j, "O")] for i in range(self.size) for j in range(self.size) if self.board[i][j]==" "]
            if len(arr):
                sorted_data = sorted(arr, key=lambda x: len(x[1]))
                for x in sorted_data:
                    print(x)
                i, j = sorted_data[-1][0]
                b = sorted_data[-1][1]
                self.board[i][j] = 'O'
                self.remove_index_from_list(self.DEFENSE, i, j, 1)
                self.remove_index_from_list(self.ATTACK, i, j, 0)
                
                self.ATTACK.extend(b)
                self.ATTACK = sorted(self.ATTACK, key=len)
                return
            # else:
            #     messagebox.showinfo("Game Over", "No winner!\nPlease try again.")
                # self.reset_game()
            return
            
        if len(self.ATTACK) > 0:
            if len(self.ATTACK[0]) == 1: # in this case the ai will win the game.
                i, j = self.ATTACK[0][0]
                self.board[i][j] = "O"
                return
        if len(self.DEFENSE)>0:    
            i,j=0,0
            flag=False
            if len(self.DEFENSE[0]) == 1:
                i, j = self.DEFENSE[0][0]
                flag=True
            else:
                if len(self.ATTACK):
                    arr=self.find_intersection()
                    if(len(arr)):
                        i,j=arr[0]
                        flag=True
                    else:
                        i,j=self.ATTACK[0][0]
                        flag=True
            if flag:
                print('i',i,'j',j)    
                self.board[i][j] = "O"
                self.update_lists(i,j,"O")
                return
        

        # get the possibilities for O insertion for all positions in Defense list and select the one with         
        arr = [[(i, j), self.get_available_cells(i, j, "O")] for inner_tuple in self.DEFENSE for i, j in inner_tuple]
        sorted_data = sorted(arr, key=lambda x: len(x[1]))
        i, j = sorted_data[-1][0]
        b = sorted_data[-1][1]
        self.board[i][j] = 'O'
        self.remove_index_from_list(self.DEFENSE, i, j, 1)
        self.remove_index_from_list(self.ATTACK, i, j, 0)
        self.ATTACK.extend(b)
        self.ATTACK = sorted(self.ATTACK, key=len)

    # To check if there a winner or if there is no winner.
    def check_game_over(self):
        winner = self.check_winner()
        if winner:
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.reset_game()
            return True
        if all(cell != " " for row in self.board for cell in row):
            messagebox.showinfo("Game Over", "No winner!\nPlease try again.")
            self.reset_game()
            return True
        return False

    def make_move(self, event):
        col = event.x // 100
        row = event.y // 100
        if self.player_move(row, col):
            self.update_board()
            if not self.check_game_over():
                self.ai_move()
                self.update_board()
                self.check_game_over()

    def update_board(self):
        self.canvas.delete("all")  # Clear the canvas
        self.create_grid()
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == "X":
                    self.canvas.create_oval(j * 100 + 10, i * 100 + 10, j * 100 + 90, i * 100 + 90, fill="green")
                    self.canvas.create_text(j * 100 + 50, i * 100 + 50, text="X", font=("Arial", 24), fill="black")
                elif self.board[i][j] == "O":
                    self.canvas.create_oval(j * 100 + 10, i * 100 + 10, j * 100 + 90, i * 100 + 90, fill="red")
                    self.canvas.create_text(j * 100 + 50, i * 100 + 50, text="O", font=("Arial", 24), fill="black")
    
    # When the user click on reset game or there is a winner then this function will called to reset the game
    def reset_game(self):
        self.board = [[" " for _ in range(self.size)] for _ in range(self.size)]
        self.DEFENSE = []
        self.ATTACK = []
        self.update_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
