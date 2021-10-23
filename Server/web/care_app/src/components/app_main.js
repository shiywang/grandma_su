import React from 'react';
import env from "react-dotenv";
import { Layout, Menu} from 'antd';
import "antd/dist/antd.css";
import {
  SearchOutlined,
  TeamOutlined,
  UserOutlined,
} from '@ant-design/icons';
import UserList from './user_list.js'
import io from 'socket.io-client'
import {exceeded_threshold} from './device_type.js'

const { Header, Content, Footer, Sider } = Layout;
const { SubMenu } = Menu;
var randomColor = require('randomcolor'); // import the script

var public_url = "http://shiywang.asuscomm.com"
// var api_service_host   = 'http://' + env.API_SERVICE_HOST;
// var node_service_host = 'http://' + env.NODESERVER_SERVICE_HOST;
// var socketio_server = node_service_host + ':4000/';
// var api_base_url = api_service_host + ":8000/";
var socketio_server = public_url + ':30006/';
var topic_name = "userdata";
var api_base_url = public_url + ":30007/";


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
    console.log("starting");
    console.log(api_base_url)
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
      for (var key in data){
        data[key]["watch"] = exceeded_threshold(data[key].data[data[key].data.length - 1].value, data[key].device_type);  // determine whether to add to watch list
        data[key]["color"] = randomColor({luminosity: 'dark',});
        this.OnlineSeniors.set(key, data[key]);
      }
      this.setState({flag: !this.state.flag});  // Triggers a re-rendering
    }).catch(err => {
      console.log(err)
    });
  }

  socket_cb = data => {
    if( "device_id" in data){
      if(data.command === "ping" && "name" in data ){
        data["watch"] = exceeded_threshold(data.data[data.data.length - 1].value, data.device_type);  // determine whether to add to watch list
        data["color"] = randomColor({luminosity: 'dark',});
        console.log("New device ping received.", data);
        this.OnlineSeniors.set(data.device_id, data);
      }

      else if(data.command === "offline" && this.OnlineSeniors.has(data.device_id)){
        console.log("Device offline");
        this.OnlineSeniors.delete(data.device_id);
      }

      else if(data.command === "data" && this.OnlineSeniors.has(data.device_id)){
        console.log("Data received");
        let new_data = {"value": data.value, "time": data.time};
        this.OnlineSeniors.get(data.device_id).data.push(new_data)
        this.OnlineSeniors.get(data.device_id).watch = exceeded_threshold(
          new_data.value, 
          this.OnlineSeniors.get(data.device_id).device_type
        ); 

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
              <UserList 
                online_seniors={Array.from(this.OnlineSeniors.values()).filter(data=>data.watch == false)}
                watch_seniors={Array.from(this.OnlineSeniors.values()).filter(data=>data.watch == true)}
              />
            </div>
          </Content>
          <Footer style={{ textAlign: 'center' }}>NE Lab ©2021 Umass Amherst</Footer>
        </Layout>

      </Layout>
    );
  }
}

export default MainApp;