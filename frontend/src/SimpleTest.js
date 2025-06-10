// frontend/src/SimpleTest.js
import React, { useEffect, useState, useRef } from 'react';
import { Container, Typography, Button, TextField, Box, Card, CardContent, Grid } from '@mui/material';

function SimpleTest() {
    const [httpMessage, setHttpMessage] = useState('Fetching HTTP...');
    const [wsMessages, setWsMessages] = useState([]);
    const [wsInput, setWsInput] = useState('');
    const [wsStatus, setWsStatus] = useState('Connecting...');
    const wsRef = useRef(null); // Ref to hold the WebSocket instance

    // --- IMPORTANT: Adjust these URLs based on your environment! ---
    // If you are running on your LOCAL computer (not Codespaces):
    // const BACKEND_HTTP_URL = 'http://localhost:8000';
    // const BACKEND_WS_URL = 'ws://localhost:8000/ws/echo';

    // If you are in a CODESPACE or similar cloud environment:
    // 1. Go to the "Ports" tab in your Codespace VS Code interface.
    // 2. Find the "Local Address" for Port 8000 (your FastAPI backend).
    //    It will look something like: https://port-8000-XXXXXXXX.preview.app.github.dev
    // 3. Copy that exact URL and paste it below for BACKEND_HTTP_URL.
    // 4. For BACKEND_WS_URL, use the same base URL, but change 'https://' to 'wss://'
    //    and append '/ws/echo'.

    // EXAMPLE FOR CODESPACES (REPLACE 'XXXXXXXX' WITH YOUR ACTUAL CODESPACE ID)
    const BACKEND_HTTP_URL = 'https://curly-space-orbit-9rw97jj7j54cx7q-8000.app.github.dev';
    const BACKEND_WS_URL = 'wss://curly-space-orbit-9rw97jj7j54cx7q-8000.app.github.dev/ws/echo';
// ------------------------------------------------------------------

    // ------------------------------------------------------------------


    // --- HTTP Test ---
    useEffect(() => {
        const fetchHttpData = async () => {
            try {
                const response = await fetch(BACKEND_HTTP_URL);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                setHttpMessage(`HTTP Success: ${data.message} (Server Time: ${data.server_time})`);
            } catch (error) {
                setHttpMessage(`HTTP Error: ${error.message}. Is backend running on ${BACKEND_HTTP_URL}?`);
                console.error("HTTP fetch error:", error);
            }
        };

        fetchHttpData();
    }, []); // Run once on mount

    // --- WebSocket Test ---
    useEffect(() => {
        const wsUrl = BACKEND_WS_URL; // Use the adjusted URL from above

        wsRef.current = new WebSocket(wsUrl);

        wsRef.current.onopen = () => {
            console.log('WebSocket Connected!');
            setWsStatus('Connected!');
            setWsMessages(prev => [...prev, { type: 'system', text: 'WebSocket Connected!' }]);
        };

        wsRef.current.onmessage = (event) => {
            console.log('WS Message:', event.data);
            setWsMessages(prev => [...prev, { type: 'server', text: event.data }]);
        };

        wsRef.current.onclose = (event) => {
            console.log('WebSocket Disconnected:', event);
            setWsStatus(`Disconnected: Code ${event.code}`);
            setWsMessages(prev => [...prev, { type: 'system', text: `WebSocket Disconnected: Code ${event.code}` }]);
        };

        wsRef.current.onerror = (error) => {
            console.error('WebSocket Error:', error);
            setWsStatus('Error! Check console.');
            setWsMessages(prev => [...prev, { type: 'system', text: `WebSocket Error: ${error.message || 'Unknown'}` }]);
        };

        // Cleanup: Close WebSocket when component unmounts
        return () => {
            if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
                console.log('Closing WebSocket...');
                wsRef.current.close();
            }
        };
    }, []); // Run once on mount

    const sendWsMessage = () => {
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            wsRef.current.send(wsInput);
            setWsMessages(prev => [...prev, { type: 'client', text: `You: ${wsInput}` }]);
            setWsInput('');
        } else {
            setWsMessages(prev => [...prev, { type: 'system', text: 'WebSocket not open. Cannot send message.' }]);
        }
    };

    return (
        <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
            <Typography variant="h4" gutterBottom>
                Simple API & WebSocket Test
            </Typography>

            <Grid container spacing={3}>
                {/* HTTP Test Card */}
                <Grid item xs={12}>
                    <Card variant="outlined">
                        <CardContent>
                            <Typography variant="h6">HTTP API Test (Root Path `/`)</Typography>
                            <Typography variant="body1" color="text.secondary">
                                Status: {httpMessage}
                            </Typography>
                            <Typography variant="caption" sx={{ mt: 1 }}>
                                Try visiting {BACKEND_HTTP_URL} in your browser directly.
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                {/* WebSocket Test Card */}
                <Grid item xs={12}>
                    <Card variant="outlined">
                        <CardContent>
                            <Typography variant="h6">WebSocket Test (`/ws/echo`)</Typography>
                            <Typography variant="body2" color="text.secondary">
                                Status: {wsStatus}
                            </Typography>
                            {/* Corrected line 128: Added missing closing curly brace '}' */}
                            <Box sx={{ my: 2, maxHeight: '200px', overflowY: 'auto', border: '1px solid #eee', p: 1 }}>
                                {wsMessages.map((msg, index) => (
                                    <Typography key={index} variant="body2"
                                        color={msg.type === 'system' ? 'text.secondary' : msg.type === 'client' ? 'primary' : 'text.primary'}
                                        sx={{ fontStyle: msg.type === 'system' ? 'italic' : 'normal' }}>
                                        {msg.text}
                                    </Typography>
                                ))}
                            </Box>
                            <Box sx={{ display: 'flex', gap: 1 }}>
                                <TextField
                                    label="Message to Server"
                                    variant="outlined"
                                    size="small"
                                    fullWidth
                                    value={wsInput}
                                    onChange={(e) => setWsInput(e.target.value)}
                                    onKeyPress={(e) => {
                                        if (e.key === 'Enter') {
                                            sendWsMessage();
                                        }
                                    }}
                                />
                                <Button variant="contained" onClick={sendWsMessage}>Send</Button>
                            </Box>
                            <Typography variant="caption" sx={{ mt: 1 }}>
                                WebSocket URL: {BACKEND_WS_URL.replace('ws://localhost', 'wss://YOUR_CODESPACE_URL')}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Container>
    );
}

export default SimpleTest;