import streamlit as st
import time
import random
from datetime import datetime
import sqlite3
import os
from typing import Dict, List, Tuple, Optional

# Page configuration
st.set_page_config(
    page_title="Crossword Battle Game",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling with updated font color for white boxes
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    
    .game-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .score-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        border-left: 4px solid #007bff;
        margin-bottom: 1rem;
        color: #000000; /* Set font color to black */
    }
    
    .ai-score-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        border-left: 4px solid #dc3545;
        margin-bottom: 1rem;
        color: #000000; /* Set font color to black */
    }
    
    .crossword-grid {
        background: white;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        color: #000000; /* Set font color to black */
    }
    
    .clue-card {
        background: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
        color: #000000; /* Set font color to black */
    }
    
    .clue-card:hover {
        background: #f8f9fa;
        border-color: #007bff;
        color: #000000; /* Ensure hover state text is black */
    }
    
    .clue-card strong, .clue-card small {
        color: #000000; /* Ensure nested elements have black text */
    }
    
    .feedback-correct {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .feedback-incorrect {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    
    .winner-banner {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

class CrosswordData:
    """Crossword puzzle data and management"""
    
    PUZZLES = {
        'easy': {
            'grid_size': (8, 8),
            'clues': [
                {'id': 1, 'clue': 'Domestic animal that barks', 'answer': 'DOG', 'row': 0, 'col': 0, 'direction': 'across', 'points': 5},
                {'id': 2, 'clue': 'Feline pet', 'answer': 'CAT', 'row': 2, 'col': 0, 'direction': 'across', 'points': 5},
                {'id': 3, 'clue': 'Color of the sky', 'answer': 'BLUE', 'row': 4, 'col': 1, 'direction': 'across', 'points': 10},
                {'id': 4, 'clue': 'Opposite of hot', 'answer': 'COLD', 'row': 0, 'col': 5, 'direction': 'down', 'points': 10},
                {'id': 5, 'clue': 'Large body of water', 'answer': 'SEA', 'row': 6, 'col': 2, 'direction': 'across', 'points': 5},
            ]
        },
        'medium': {
            'grid_size': (10, 10),
            'clues': [
                {'id': 1, 'clue': 'Capital of France', 'answer': 'PARIS', 'row': 0, 'col': 0, 'direction': 'across', 'points': 15},
                {'id': 2, 'clue': 'Largest planet in our solar system', 'answer': 'JUPITER', 'row': 2, 'col': 1, 'direction': 'across', 'points': 20},
                {'id': 3, 'clue': 'Programming language named after a snake', 'answer': 'PYTHON', 'row': 4, 'col': 0, 'direction': 'across', 'points': 20},
                {'id': 4, 'clue': 'Chemical symbol for gold', 'answer': 'AU', 'row': 6, 'col': 3, 'direction': 'down', 'points': 15},
                {'id': 5, 'clue': 'Author of Romeo and Juliet', 'answer': 'SHAKESPEARE', 'row': 7, 'col': 0, 'direction': 'across', 'points': 25},
            ]
        },
        'hard': {
            'grid_size': (12, 12),
            'clues': [
                {'id': 1, 'clue': 'Study of the fundamental nature of reality', 'answer': 'METAPHYSICS', 'row': 0, 'col': 0, 'direction': 'across', 'points': 30},
                {'id': 2, 'clue': 'Mathematical constant approximately 3.14159', 'answer': 'PI', 'row': 2, 'col': 5, 'direction': 'down', 'points': 25},
                {'id': 3, 'clue': 'Process by which plants make food', 'answer': 'PHOTOSYNTHESIS', 'row': 4, 'col': 0, 'direction': 'across', 'points': 35},
                {'id': 4, 'clue': 'Ancient Greek philosopher taught by Plato', 'answer': 'ARISTOTLE', 'row': 6, 'col': 2, 'direction': 'across', 'points': 30},
                {'id': 5, 'clue': 'Quantum physics principle about uncertainty', 'answer': 'HEISENBERG', 'row': 8, 'col': 1, 'direction': 'across', 'points': 35},
            ]
        }
    }
    
    @classmethod
    def get_puzzle(cls, difficulty: str) -> Dict:
        return cls.PUZZLES.get(difficulty, cls.PUZZLES['easy'])

class AIPlayer:
    """AI opponent with difficulty-based behavior"""
    
    def __init__(self, difficulty: str = 'medium'):
        self.difficulty = difficulty
        self.accuracy_rates = {
            'easy': 0.7,
            'medium': 0.85,
            'hard': 0.95
        }
        self.thinking_times = {
            'easy': (2, 4),
            'medium': (3, 6),
            'hard': (4, 8)
        }
    
    def select_clue(self, available_clues: List[Dict]) -> Optional[Dict]:
        """Select a clue based on AI difficulty"""
        if not available_clues:
            return None
        
        if self.difficulty == 'easy':
            # Prefer shorter words
            return min(available_clues, key=lambda x: len(x['answer']))
        elif self.difficulty == 'hard':
            # Prefer high-point clues
            return max(available_clues, key=lambda x: x['points'])
        else:
            # Random selection for medium
            return random.choice(available_clues)
    
    def attempt_answer(self, clue: Dict) -> bool:
        """Attempt to answer a clue based on AI accuracy"""
        accuracy = self.accuracy_rates[self.difficulty]
        return random.random() < accuracy

def init_database():
    """Initialize SQLite database for game statistics"""
    conn = sqlite3.connect('crossword_stats.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_score INTEGER,
            ai_score INTEGER,
            difficulty TEXT,
            winner TEXT,
            game_date TIMESTAMP,
            duration_seconds INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_games INTEGER DEFAULT 0,
            total_wins INTEGER DEFAULT 0,
            total_score INTEGER DEFAULT 0,
            win_streak INTEGER DEFAULT 0,
            best_streak INTEGER DEFAULT 0,
            last_updated TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_game_stats(player_score: int, ai_score: int, difficulty: str, winner: str, duration: int):
    """Save game statistics to database"""
    conn = sqlite3.connect('crossword_stats.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO game_stats (player_score, ai_score, difficulty, winner, game_date, duration_seconds)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (player_score, ai_score, difficulty, winner, datetime.now(), duration))
    
    # Update player stats
    cursor.execute('SELECT * FROM player_stats WHERE id = 1')
    stats = cursor.fetchone()
    
    if stats:
        total_games = stats[1] + 1
        total_wins = stats[2] + (1 if winner == 'Player' else 0)
        total_score = stats[3] + player_score
        current_streak = stats[4]
        best_streak = stats[5]
        
        if winner == 'Player':
            current_streak += 1
            best_streak = max(best_streak, current_streak)
        else:
            current_streak = 0
        
        cursor.execute('''
            UPDATE player_stats 
            SET total_games = ?, total_wins = ?, total_score = ?, 
                win_streak = ?, best_streak = ?, last_updated = ?
            WHERE id = 1
        ''', (total_games, total_wins, total_score, current_streak, best_streak, datetime.now()))
    else:
        cursor.execute('''
            INSERT INTO player_stats (total_games, total_wins, total_score, win_streak, best_streak, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (1, 1 if winner == 'Player' else 0, player_score, 1 if winner == 'Player' else 0, 1 if winner == 'Player' else 0, datetime.now()))
    
    conn.commit()
    conn.close()

def initialize_game():
    """Initialize game session state"""
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
    if 'player_score' not in st.session_state:
        st.session_state.player_score = 0
    if 'ai_score' not in st.session_state:
        st.session_state.ai_score = 0
    if 'solved_clues' not in st.session_state:
        st.session_state.solved_clues = set()
    if 'feedback_message' not in st.session_state:
        st.session_state.feedback_message = ""
    if 'feedback_type' not in st.session_state:
        st.session_state.feedback_type = ""
    if 'game_start_time' not in st.session_state:
        st.session_state.game_start_time = None
    if 'winner' not in st.session_state:
        st.session_state.winner = None
    if 'ai_thinking' not in st.session_state:
        st.session_state.ai_thinking = False

def start_new_game(difficulty: str):
    """Start a new game with selected difficulty"""
    st.session_state.game_active = True
    st.session_state.difficulty = difficulty
    st.session_state.puzzle_data = CrosswordData.get_puzzle(difficulty)
    st.session_state.ai_player = AIPlayer(difficulty)
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.solved_clues = set()
    st.session_state.feedback_message = ""
    st.session_state.feedback_type = ""
    st.session_state.game_start_time = time.time()
    st.session_state.winner = None
    st.session_state.ai_thinking = False

def check_winner():
    """Check if there's a winner"""
    if st.session_state.player_score >= 20:
        st.session_state.winner = "Player"
        return True
    elif st.session_state.ai_score >= 20:
        st.session_state.winner = "AI"
        return True
    return False

def process_player_answer(clue_id: int, answer: str):
    """Process player's answer"""
    clue = next((c for c in st.session_state.puzzle_data['clues'] if c['id'] == clue_id), None)
    
    if clue and answer.upper().strip() == clue['answer']:
        st.session_state.player_score += clue['points']
        st.session_state.solved_clues.add(clue_id)
        st.session_state.feedback_message = "Correct!"
        st.session_state.feedback_type = "correct"
        
        if not check_winner():
            st.session_state.ai_thinking = False  # No AI turn after correct answer
    else:
        st.session_state.feedback_message = "Incorrect answer"
        st.session_state.feedback_type = "incorrect"
        st.session_state.ai_thinking = True  # Trigger AI turn after incorrect answer
        st.rerun()

def ai_turn():
    """Execute AI turn"""
    if st.session_state.ai_thinking:
        available_clues = [c for c in st.session_state.puzzle_data['clues'] 
                          if c['id'] not in st.session_state.solved_clues]
        
        if available_clues:
            selected_clue = st.session_state.ai_player.select_clue(available_clues)
            
            if selected_clue and st.session_state.ai_player.attempt_answer(selected_clue):
                st.session_state.ai_score += selected_clue['points']
                st.session_state.solved_clues.add(selected_clue['id'])
                st.session_state.feedback_message = f"AI solved: {selected_clue['clue']} → {selected_clue['answer']}"
                st.session_state.feedback_type = "ai_correct"
                check_winner()
        
        st.session_state.ai_thinking = False

def main():
    """Main Streamlit application"""
    
    # Initialize database and game state
    init_database()
    initialize_game()
    
    # Game header
    st.markdown("""
    <div class="game-header">
        <h1>🧩 Crossword Battle Game</h1>
        <p>Compete against AI to solve crossword puzzles and reach 20 points first!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Handle AI turn if needed
    if st.session_state.get('ai_thinking', False):
        ai_turn()
        st.rerun()
    
    # Game setup or active game
    if not st.session_state.game_active:
        st.markdown("### Choose Your Challenge")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🟢 Easy Mode", use_container_width=True):
                start_new_game('easy')
                st.rerun()
            st.markdown("*Short words, basic clues*")
        
        with col2:
            if st.button("🟡 Medium Mode", use_container_width=True):
                start_new_game('medium')
                st.rerun()
            st.markdown("*Moderate difficulty*")
        
        with col3:
            if st.button("🔴 Hard Mode", use_container_width=True):
                start_new_game('hard')
                st.rerun()
            st.markdown("*Complex clues, long words*")
        
        # Display statistics
        st.markdown("---")
        st.markdown("### Your Statistics")
        
        try:
            conn = sqlite3.connect('crossword_stats.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM player_stats WHERE id = 1')
            stats = cursor.fetchone()
            conn.close()
            
            if stats:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Games", stats[1])
                with col2:
                    win_rate = (stats[2] / stats[1] * 100) if stats[1] > 0 else 0
                    st.metric("Win Rate", f"{win_rate:.1f}%")
                with col3:
                    st.metric("Current Streak", stats[4])
                with col4:
                    st.metric("Best Streak", stats[5])
            else:
                st.info("Play your first game to see statistics!")
        except:
            st.info("Play your first game to see statistics!")
    
    else:
        # Active game interface
        if st.session_state.winner:
            # Winner announcement
            if st.session_state.winner == "Player":
                st.markdown("""
                <div class="winner-banner">
                    <h2>🎉 Congratulations! You Won! 🎉</h2>
                    <p>You reached 20 points first!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="winner-banner">
                    <h2>🤖 AI Wins This Round!</h2>
                    <p>Better luck next time!</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Save game statistics
            if 'stats_saved' not in st.session_state:
                duration = int(time.time() - st.session_state.game_start_time)
                save_game_stats(
                    st.session_state.player_score,
                    st.session_state.ai_score,
                    st.session_state.difficulty,
                    st.session_state.winner,
                    duration
                )
                st.session_state.stats_saved = True
            
            if st.button("🎮 Play Again", use_container_width=True):
                st.session_state.game_active = False
                if 'stats_saved' in st.session_state:
                    del st.session_state.stats_saved
                st.rerun()
        
        else:
            # Score display
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="score-card">
                    <h3>👤 Your Score</h3>
                    <h2>{st.session_state.player_score}</h2>
                    <p>Target: 20 points</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="ai-score-card">
                    <h3>🤖 AI Score</h3>
                    <h2>{st.session_state.ai_score}</h2>
                    <p>Target: 20 points</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Feedback message
            if st.session_state.feedback_message:
                if st.session_state.feedback_type == "correct":
                    st.markdown(f"""
                    <div class="feedback-correct">
                        <strong>{st.session_state.feedback_message}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                elif st.session_state.feedback_type == "incorrect":
                    st.markdown(f"""
                    <div class="feedback-incorrect">
                        <strong>{st.session_state.feedback_message}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info(st.session_state.feedback_message)
            
            # Clues display
            st.markdown("### Available Clues")
            
            available_clues = [c for c in st.session_state.puzzle_data['clues'] 
                             if c['id'] not in st.session_state.solved_clues]
            
            if available_clues:
                for clue in available_clues:
                    with st.container():
                        st.markdown(f"""
                        <div class="clue-card">
                            <strong>{clue['id']}. {clue['clue']}</strong><br>
                            <small>{clue['direction'].title()} • {len(clue['answer'])} letters • {clue['points']} points</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            answer = st.text_input(
                                f"Your answer for clue {clue['id']}:",
                                key=f"answer_{clue['id']}",
                                placeholder=f"Enter {len(clue['answer'])} letter word..."
                            )
                        with col2:
                            if st.button(f"Submit", key=f"submit_{clue['id']}"):
                                if answer.strip():
                                    process_player_answer(clue['id'], answer)
                                    st.rerun()
                        
                        st.markdown("---")
            else:
                st.success("All clues solved! Great job!")
            
            # Game controls
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 New Game", use_container_width=True):
                    st.session_state.game_active = False
                    st.rerun()

if __name__ == "__main__":
    main()
