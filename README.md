# Crossword Battle Game - Streamlit Version

A modern, interactive crossword battle game built with Streamlit where players compete against AI opponents to solve puzzles and reach 100 points first.

## 🎮 Game Features

- **Three Difficulty Levels**: Easy, Medium, and Hard with different AI behaviors
- **Modern UI Design**: Beautiful gradient headers and card-based layout
- **Real-time Scoring**: Live score updates as you play
- **Visual Feedback**: Clear correct/incorrect answer notifications
- **AI Opponent**: Smart AI that adapts strategy based on difficulty
- **Statistics Tracking**: Persistent game statistics and win streaks
- **Responsive Design**: Works perfectly on desktop and mobile

## 🚀 Quick Deploy to Streamlit Cloud

### Step 1: Upload to GitHub
1. Create a new repository on GitHub
2. Upload all files from this folder
3. Make sure `streamlit_app.py` is in the root directory

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file: `streamlit_app.py`
6. Click "Deploy!"

Your app will be live at: `https://your-username-repo-name.streamlit.app`

## 🛠 Local Development

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

Access at: `http://localhost:8501`

## 🎯 How to Play

1. **Choose Difficulty**: Select Easy, Medium, or Hard mode
2. **Read Clues**: Each clue shows points, word length, and direction
3. **Submit Answers**: Type your answer and click Submit
4. **AI Turn**: AI automatically attempts a clue after your turn
5. **Win**: First to reach 100 points wins!

## 📊 Game Statistics

The app automatically tracks:
- Total games played
- Win percentage
- Current win streak
- Best win streak
- Game history

## 🔧 Customization

### Add New Puzzles
Edit the `CrosswordData.PUZZLES` dictionary in `streamlit_app.py`:

```python
'your_difficulty': {
    'grid_size': (10, 10),
    'clues': [
        {
            'id': 1, 
            'clue': 'Your clue text', 
            'answer': 'ANSWER', 
            'row': 0, 
            'col': 0, 
            'direction': 'across', 
            'points': 20
        }
    ]
}
```

### Adjust AI Difficulty
Modify the accuracy rates in the `AIPlayer` class:

```python
self.accuracy_rates = {
    'easy': 0.7,    # 70% accuracy
    'medium': 0.85, # 85% accuracy
    'hard': 0.95    # 95% accuracy
}
```

### Change Styling
Update the CSS in the `st.markdown()` section to customize colors, animations, and layout.

## 📁 File Structure

```
crossword-streamlit/
├── streamlit_app.py           # Main application
├── requirements.txt           # Python dependencies
├── .streamlit/
│   └── config.toml           # Streamlit configuration
└── README.md                 # This file
```

## 🎨 UI Design Features

- **Gradient Headers**: Beautiful purple gradient design
- **Score Cards**: Clean player vs AI score display
- **Visual Feedback**: Green/red feedback for answers
- **Winner Animation**: Pulsing celebration banner
- **Hover Effects**: Interactive button animations
- **Responsive Layout**: Mobile-friendly design

## 🤖 AI Behavior

### Easy Mode (70% accuracy)
- Prefers shorter words
- Slower thinking time
- More mistakes

### Medium Mode (85% accuracy)
- Random clue selection
- Moderate thinking time
- Balanced difficulty

### Hard Mode (95% accuracy)
- Targets high-point clues
- Faster thinking time
- Very few mistakes

## 🔒 Data Storage

- **SQLite Database**: Local storage for statistics
- **Session State**: Game state management
- **Persistent Stats**: Statistics survive app restarts

## 🚨 Troubleshooting

### Common Issues

1. **App won't start**: Check requirements.txt format
2. **Database errors**: Ensure write permissions
3. **Styling issues**: Clear browser cache
4. **Game state problems**: Refresh the page

### Getting Help

- Streamlit Docs: [docs.streamlit.io](https://docs.streamlit.io)
- Community: [discuss.streamlit.io](https://discuss.streamlit.io)
- App link : https://pvhjv6bxv84tyrlrfmwdct.streamlit.app/
## 📄 License

This project is open source. Feel free to customize and improve!
