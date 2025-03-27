import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Svatební Hra",
    page_icon="💍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

html_code ='''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Heart Breaker Čeština</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            touch-action: none;
            font-family: Arial, sans-serif;
        }
        #gameCanvas {
            background: #babca2;
            display: none;
        }
        .screen {
            position: fixed;
            width: 100%;
            height: 100%;
            background: rgba(186, 188, 162, 0.95);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        #welcomeScreen {
            display: flex;
        }
        #endScreen {
            display: none;
        }
        button {
            padding: 15px 30px;
            font-size: 20px;
            background: #7D6B7D;
            color: white;
            border: none;
            border-radius: 25px;
            margin-top: 20px;
            cursor: pointer;
        }
        h1 {
            color: #4a5043;
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        p {
            color: #4a5043;
            font-size: 1.2em;
        }
        #score {
            position: absolute;
            top: 20px;
            left: 20px;
            font-size: 30px;
            color: #4a5043;
            font-weight: bold;
            display: none;
        }
    </style>
</head>
<body>
    <div id="welcomeScreen" class="screen">
        <h1>Láskobour</h1>
        <p>Láska bourá všechny zdi - zkuste to</p>
        <button onclick="startGame()">Začít hru</button>
        <p>Made with❤️ K & J 👰🤵</p>
    </div>

    <div id="endScreen" class="screen">
        <h1 id="endTitle"></h1>
        <p id="endScore"></p>
        <button onclick="startGame()">Hrát znovu</button>
    </div>

    <div id="score">Skóre: 0</div>
    <canvas id="gameCanvas"></canvas>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const scoreElement = document.getElementById('score');
        const welcomeScreen = document.getElementById('welcomeScreen');
        const endScreen = document.getElementById('endScreen');
        const endTitle = document.getElementById('endTitle');
        const endScore = document.getElementById('endScore');

        // Game variables
        let paddleWidth = 100;
        let paddleHeight = 20;
        let ballSize = 30;
        let paddleX, ball, score, gameActive, blocks;

        function initGame() {
            paddleX = canvas.width/2 - paddleWidth/2;
            ball = {
                x: canvas.width/2,
                y: canvas.height - 100,
                speedX: 5,
                speedY: -5
            };
            score = 0;
            gameActive = true;
            createBlocks();
            scoreElement.textContent = `Skóre: ${score}`;
        }

        function createBlocks() {
            blocks = [];
            const blockRows = 3;
            const blockCols = 5;
            const blockWidth = canvas.width / blockCols;
            const blockHeight = 30;
            
            for(let i = 0; i < blockRows; i++) {
                for(let j = 0; j < blockCols; j++) {
                    blocks.push({
                        x: j * blockWidth,
                        y: i * blockHeight + 50,
                        width: blockWidth - 5,
                        height: blockHeight - 5,
                        active: true
                    });
                }
            }
        }

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }

        // Controls
        let leftPressed = false;
        let rightPressed = false;
        let touchX = null;

        document.addEventListener('keydown', (e) => {
            if(e.key === 'ArrowLeft') leftPressed = true;
            if(e.key === 'ArrowRight') rightPressed = true;
        });

        document.addEventListener('keyup', (e) => {
            if(e.key === 'ArrowLeft') leftPressed = false;
            if(e.key === 'ArrowRight') rightPressed = false;
        });

        canvas.addEventListener('touchstart', (e) => {
            e.preventDefault();
            touchX = e.touches[0].clientX;
        });

        canvas.addEventListener('touchmove', (e) => {
            e.preventDefault();
            touchX = e.touches[0].clientX;
        });

        function gameLoop() {
            if(!gameActive) return;

            // Move paddle
            if(leftPressed || (touchX && touchX < paddleX + paddleWidth/2)) {
                paddleX -= 7;
            }
            if(rightPressed || (touchX && touchX > paddleX + paddleWidth/2)) {
                paddleX += 7;
            }

            paddleX = Math.max(0, Math.min(canvas.width - paddleWidth, paddleX));

            // Move ball
            ball.x += ball.speedX;
            ball.y += ball.speedY;

            // Collisions
            if(ball.x < 0 || ball.x > canvas.width) ball.speedX = -ball.speedX;
            if(ball.y < 0) ball.speedY = -ball.speedY;

            // Paddle collision
            if(ball.y > canvas.height - paddleHeight - ballSize/2 &&
               ball.x > paddleX && ball.x < paddleX + paddleWidth) {
                ball.speedY = -Math.abs(ball.speedY);
                ball.speedX += (Math.random() - 0.5) * 2;
            }

            // Block collisions
            blocks.forEach(block => {
                if(block.active && ball.x > block.x && ball.x < block.x + block.width &&
                   ball.y > block.y && ball.y < block.y + block.height) {
                    block.active = false;
                    ball.speedY = -ball.speedY;
                    score += 10;
                    scoreElement.textContent = `Skóre: ${score}`;
                }
            });

            // End conditions
            if(ball.y > canvas.height) endGame(false);
            if(blocks.every(block => !block.active)) endGame(true);

            // Drawing
            ctx.fillStyle = '#babca2';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Paddle
            ctx.fillStyle = '#7D6B7D';
            ctx.fillRect(paddleX, canvas.height - paddleHeight, paddleWidth, paddleHeight);

            // Ball
            ctx.font = `${ballSize}px Arial`;
            ctx.fillText('❤️', ball.x - ballSize/2, ball.y + ballSize/2);

            // Blocks
            blocks.forEach(block => {
                if(block.active) {
                    ctx.fillStyle = '#A88FAC';
                    ctx.fillRect(block.x, block.y, block.width, block.height);
                }
            });

            requestAnimationFrame(gameLoop);
        }

        function endGame(won) {
            gameActive = false;
            canvas.style.display = 'none';
            scoreElement.style.display = 'none';
            endScreen.style.display = 'flex';
            endTitle.textContent = won ? "Vyhráli jste! ❤️" : "Konec Hry 💔";
            endScore.textContent = `Skóre: ${score}`;
        }

        function startGame() {
            welcomeScreen.style.display = 'none';
            endScreen.style.display = 'none';
            canvas.style.display = 'block';
            scoreElement.style.display = 'block';
            resizeCanvas();
            initGame();
            gameActive = true;
            gameLoop();
        }

        // Initial setup
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();
    </script>
</body>
</html>
'''

custom_css = """
<style>
    /* Background color for the app */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* Title styling */
    h1 {
        font-family: 'Playfair Display', serif;
        color: #D8A9A4 !important;
        text-align: center;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        font-size: 14px;
        color: #6c757d;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #dee2e6;
    }
    
    /* Header styling */
    .header {
        text-align: center;
        font-size: 18px;
        color: #4a5043;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #dee2e6;
    }
    
    /* Emoticon styling */
    .emoticons {
        text-align: center;
        font-size: 24px;
        margin: 10px 0;
    }
    
    /* Decoration styling - for the emoticons */
    .decoration {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        font-size: 28px;
        padding: 15px 0;
        width: 100%;
        margin: 10px auto;
    }
</style>
"""

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Header with decorative elements
st.markdown('<div class="decoration">💍 💝 🕊️</div>', unsafe_allow_html=True)

st.title("Hra pro svatební web")

st.markdown('<div class="game-container">', unsafe_allow_html=True)
components.html(html_code, height=600, scrolling=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer with decorative elements
st.markdown('<div class="decoration">🥂 💐 ❤️</div>', unsafe_allow_html=True)