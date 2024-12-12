import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5001',
  headers: {
    'Content-Type': 'application/json', // 必要なヘッダー
  },
});


// ゲームの初期化
export const initializeGame = async () => {
  try {
    const response = await api.post('/initialize');
    return response.data.message;
  } catch (error) {
    console.error('Error initializing game:', error);
    throw error;
  }
};

// チャットメッセージの送信
export const chatWithGPT = async (message) => {
  try {
    const response = await api.post('/chat', { message });
    return response.data.response;
  } catch (error) {
    console.error('Error chatting with GPT:', error);
    throw error;
  }
};
