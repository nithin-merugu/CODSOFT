import streamlit as st
from tictactoe_game import TicTacToe, get_best_move

st.set_page_config(page_title="Tic-Tac-Toe AI", page_icon="🎮")

st.title("Tic-Tac-Toe vs AI")

# Initialize session state
if 'game' not in st.session_state:
    st.session_state.game = TicTacToe()
    st.session_state.board = st.session_state.game.board
    st.session_state.game_over = False
    st.session_state.winner = None

# Function to handle player's move
def player_move(i):
    if st.session_state.board[i] == ' ' and not st.session_state.game_over:
        st.session_state.game.make_move(i, 'X')
        st.session_state.board = st.session_state.game.board
        
        if st.session_state.game.current_winner:
            st.session_state.game_over = True
            st.session_state.winner = 'Player'
        elif st.session_state.game.empty_squares():
            ai_move()
        else:
            st.session_state.game_over = True
            st.session_state.winner = 'Tie'

# Function to handle AI's move
def ai_move():
    move = get_best_move(st.session_state.game)
    st.session_state.game.make_move(move, 'O')
    st.session_state.board = st.session_state.game.board
    
    if st.session_state.game.current_winner:
        st.session_state.game_over = True
        st.session_state.winner = 'AI'
    elif not st.session_state.game.empty_squares():
        st.session_state.game_over = True
        st.session_state.winner = 'Tie'

# Create the game board
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7, col8, col9 = st.columns(3)

board_buttons = [
    col1.button(st.session_state.board[0], key=0, on_click=player_move, args=(0,)),
    col2.button(st.session_state.board[1], key=1, on_click=player_move, args=(1,)),
    col3.button(st.session_state.board[2], key=2, on_click=player_move, args=(2,)),
    col4.button(st.session_state.board[3], key=3, on_click=player_move, args=(3,)),
    col5.button(st.session_state.board[4], key=4, on_click=player_move, args=(4,)),
    col6.button(st.session_state.board[5], key=5, on_click=player_move, args=(5,)),
    col7.button(st.session_state.board[6], key=6, on_click=player_move, args=(6,)),
    col8.button(st.session_state.board[7], key=7, on_click=player_move, args=(7,)),
    col9.button(st.session_state.board[8], key=8, on_click=player_move, args=(8,)),
]

# Display game status
if st.session_state.game_over:
    if st.session_state.winner == 'Tie':
        st.write("It's a tie!")
    else:
        st.write(f"{st.session_state.winner} wins!")
    
    if st.button("Play Again"):
        st.session_state.game = TicTacToe()
        st.session_state.board = st.session_state.game.board
        st.session_state.game_over = False
        st.session_state.winner = None
        st.experimental_rerun()
else:
    st.write("Your turn! Click on an empty square to make your move.")