import React from 'react';
import { Layout,  Typography, Row, Col, Divider} from 'antd';
import "antd/dist/antd.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowsAltH, } from '@fortawesome/free-solid-svg-icons'
import GaugeChart from 'react-gauge-chart'

const { Text } = Typography;

export class Device_Title extends React.Component {
  state = {
    collapsed: false,
  };

  constructor(props, device_data ) {
    super(props);
    this.title = device_data.title;
    this.trigger = device_data.trigger
    this.title_icon = device_data.title_icon
  }

  render() {
    return (
        <>
            <Row justify='space-around'>
                <Col >
                    <Text code style={{}}>R-R</Text>
                </Col>
            </Row>
            <Row justify='space-around'>
                <Col flexDirection='row' >
                    <Text strong style={{fontSize: 24}}>
                        {this.props.data.data[ this.props.data.data.length - 1]}
                    </Text>
                </Col>
            </Row>
        </>
    );
  }
}

export class RR_Device_Title extends Device_Title {
    constructor(props){
        let device_data = {
            "title": "R-R",
            "trigger": 1200, 
            "title_icon": faArrowsAltH,
        }
        super(props, device_data)
    }
 }

const styles = {
}
