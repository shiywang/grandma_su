import React from 'react';
import { Avatar,  Typography, Row, Col, Divider} from 'antd';
import "antd/dist/antd.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMars, faVenus, faBatteryFull, faBatteryThreeQuarters, faBatteryHalf, faBatteryQuarter, faBatteryEmpty} from '@fortawesome/free-solid-svg-icons'
//import {Device_Title, RR_Device_Title} from './device_type.js'

const { Text } = Typography;
var randomColor = require('randomcolor'); // import the script

class SeniorUser extends React.Component {
  state = {
    collapsed: false,
  };

  constructor(props){
    super(props);
  }

  componentDidMount(){
    this.mycolor = randomColor()
  }

  senior_battery_icon = (val)=>{
    if(val < 10){return <FontAwesomeIcon color='red' style={styles.batteryIcon} icon={faBatteryEmpty} size="lg"/>}
    else if(val < 35){return <FontAwesomeIcon style={styles.batteryIcon} icon={faBatteryQuarter} size="lg"/> }
    else if(val < 60){return <FontAwesomeIcon style={styles.batteryIcon} icon={faBatteryHalf} size="lg"/> }
    else if(val < 90){return <FontAwesomeIcon style={styles.batteryIcon} icon={faBatteryThreeQuarters} size="lg"/>}
    else{
      return <FontAwesomeIcon style={styles.batteryIcon} icon={faBatteryFull} size={32}/>
    }
  };

  senior_object = () => {
    return (  
      <>{ 
      this.props.element_size === 1 ?

      <div> {/***  Normal Mode ****/}
        <Row>
          {/* Avatar */}
          <Col flex={1}> 
            <Avatar size={24} style={{ marginRight:5, backgroundColor: this.mycolor}}  >{this.props.data.name[0]}</Avatar>           
          </Col>

          {/* Name and Device ID*/}
          <Col flex={5}>  
            <Row> <Text strong style={{fontSize: 13}}> {this.props.data.name.substr(0, 16)} </Text> </Row>
            <Row justify='space-around'> 
              <Col flex={1}>
                <Text code >
                    {this.props.data.gender === 'male' ?
                        <FontAwesomeIcon icon={faMars} size="1x"/> :
                        <FontAwesomeIcon icon={faVenus} size="1x"/>
                    }
                </Text>
              </Col >
              <Col flex={5}>
                <Text disabled style={{fontSize: 10, textAlign: 'center'}}> {'@'+this.props.data.device_id} </Text> 
              </Col>
            </Row>
          </Col>

          {/* Device Data */}
          <Col flex={3}>
            <Row justify='space-around'>
              <Col  >
                <Row justify='space-around'>
                  <Text code style={{textAlign: 'center'}}> 
                    {this.props.data.battery + '%' + '🔋'}  
                  </Text>
                </Row>
              </Col>
              <Col >
                  <Divider type="vertical" style={{ margin: 0, height: '100%'}}/>
              </Col>
              <Col > 
                <Row justify='space-around'>
                    <Col >
                        <Text code style={{}}>{this.props.data.device_type}</Text>
                    </Col>
                </Row>
                <Row justify='space-around'>
                    <Col  >
                        <Text strong style={{fontSize: 20}}>
                            {this.props.data.data[ this.props.data.data.length - 1].value}
                        </Text>
                    </Col>
                </Row>
              </Col>
            </Row>
          </Col>
        </Row>      
      </div>

      : 
      <div> {/***  Bulk Mode ****/}
        <Row justify='space-around'>
          <Col> 
            <Text style={{fontSize: 10, textAlign: 'center'}}> {'@'+this.props.data.device_id} </Text> 
          </Col>
          <Col><Divider type="vertical" style={{height: "100%"}} /></Col>
          <Col> 
            <Text code strong style={{fontSize: 14, textAlign: 'center'}}> 
              R-R:  {this.props.data.data[ this.props.data.data.length - 1].value}
            </Text> 
          </Col>
        </Row>
      </div>
    }</>
    ) 
  }


  render() {
    return (
      <div>
        <div 
          style = { this.props.element_size === 1 ? styles.card_div : styles.card_div_small} 
          flex ='auto'
        >
          {this.senior_object()}
        </div>
        
      </div>
    );
  }
}

export default SeniorUser;


const styles = {
  card_div:{
    borderRadius: 10, 
    margin: 5,
    padding: 10,
    backgroundColor: 'white',
    boxShadow: "2px 2px 2px 2px #dcdcdc"
  },
  card_div_small:{
    borderRadius: 5, 
    margin: 5,
    padding: 5,
    backgroundColor: 'white',
    boxShadow: "2px 2px 2px 2px #dcdcdc"
  },
  batteryIcon:{
     marginLeft: 8,
  }
}

