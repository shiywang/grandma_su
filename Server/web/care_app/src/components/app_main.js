import React from 'react';
import { Layout, Menu} from 'antd';
import "antd/dist/antd.css";
import {
  SearchOutlined,
  TeamOutlined,
  UserOutlined,
} from '@ant-design/icons';
import UserList from './user_list.js'
import io from 'socket.io-client'
import { faDiceFive } from '@fortawesome/free-solid-svg-icons';

const { Header, Content, Footer, Sider } = Layout;
const { SubMenu } = Menu;

var socketio_server = 'http://127.0.0.1:4000/';
var topic_name = "userdata";
var api_base_url = "http://127.0.0.1:8002/"

let headers = new Headers();
headers.append('Accept', 'application/json');

const temp_user = {
  "name": "Jeffery Homes",
  "age": 78,
  "gender": "male",
  "device_id": "AG82DD4",
  "device_type": "ECG",
  "battery": 50,
  "data": [{"value": 35, "time": 0}],
}

const max_array_len = 10;

class MainApp extends React.Component {
  
  constructor(props){
    super(props);
    console.log("starting")
    this.state = {
      collapsed: false,
      flag: false
    };
    this.OnlineSeniors =  new Map();
    //this.OnlineSeniors.set(temp_user.device_id, temp_user);
  }

  componentDidMount(){
    let socket = io(socketio_server, {transports: ['websocket', 'polling', 'flashsocket']});
    socket.on(topic_name, this.socket_cb);

    fetch(api_base_url + 'get-online-seniors/', {
        method: 'GET',
        headers: headers
    })
    .then((response) => response.json())
    .then((data) => {
      for (var key  in data){
        this.OnlineSeniors.set(key, data[key]);
      }
      this.setState({flag: !this.state.flag});  // Triggers a re-rendering
    });
  }

  socket_cb = data => {
    if( "device_id" in data){
      if(data.command === "ping" && "name" in data ){
        console.log("New device ping received.");
        this.OnlineSeniors.set(data.device_id, data);
      }

      else if(data.command === "offline" && this.OnlineSeniors.has(data.device_id)){
        console.log("Device offline");
        this.OnlineSeniors.delete(data.device_id);
      }

      else if(data.command === "data" && this.OnlineSeniors.has(data.device_id)){
        console.log("Data received");
        console.log(data);
        let new_data = {"value": data.value, "time": data.time};
        this.OnlineSeniors.get(data.device_id).data.push(new_data)

        // Maintain array size
        if(this.OnlineSeniors.get(data.device_id).data.length > max_array_len){
          this.OnlineSeniors.get(data.device_id).data.shift()
        }
      }
    }
    this.setState({flag: !this.state.flag});  // Triggers a re-rendering
  }

  onCollapse = collapsed => {
    console.log(collapsed);
    this.setState({ collapsed });
  };

  render() {
    const { collapsed } = this.state;
    return (
      <Layout style={{ minHeight: '100vh' }}>
        <Sider collapsible collapsed={collapsed} onCollapse={this.onCollapse}>
          <div style={{height: 60}}> </div>
          <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline">
            <Menu.Item key="1" icon={<TeamOutlined />}>
              Online Users
            </Menu.Item>
            <Menu.Item key="2" icon={<SearchOutlined />}>
              Search 
            </Menu.Item>
            <Menu.Item key="3" icon={<UserOutlined />}>
              Add New User
            </Menu.Item>
          </Menu>
        </Sider>

        <Layout className="site-layout">
          <Header className="site-layout-background" style={{ padding: 0 }} />
          <Content style={{ margin: '0 16px' }}>
            <div className="site-layout-background" style={{ padding: 24, minHeight: 360 }}>
              <UserList online_seniors={Array.from(this.OnlineSeniors.values())}/>
            </div>
          </Content>
          <Footer style={{ textAlign: 'center' }}>NE Lab ©2021 Umass Amherst</Footer>
        </Layout>

      </Layout>
    );
  }
}

export default MainApp;