import { message } from 'antd';
import React, { Component } from 'react';
import { w3cwebsocket as W3CWebSocket } from 'websocket';

const client = new W3CWebSocket('ws://127.0.0.1:8000/ws/sensordata/RR');

class WSClient extends Component {
  componentWillMount() {
    client.onopen = () => {
      console.log('WebSocket Client Connected');
    };
    client.onmessage = (message) => {
      alert(message)
      console.log(message);
    };
    
    client.onclose = (message) => {
      console.log(message);
    };
    client.onerror = (message) => {
      console.log(message);
    };
  }
  
  render() {
    return (
      <div>
        
      </div>
    );
  }
}

export default WSClient;
