import React from 'react';
import { List} from 'antd';
import "antd/dist/antd.css";
import SeniorUser from './senior_user.js';


class UserList extends React.Component {
  

  constructor(props){
    super(props);
    this.state = {
      collapsed: false,
      element_size: 1
    };
  }


  render() {
    return (
      <div>
        <List
            grid={this.state.element_size === 1 ? 
                {gutter: 16, xs: 1, sm: 2, md: 3, lg: 3, xl: 4, xxl: 6,} : 
                {gutter: 16, xs: 1, sm: 2, md: 3, lg: 3, xl: 4, xxl: 9,} 
            }
            dataSource={this.props.online_seniors} 

            renderItem={item => (
                <SeniorUser data={item} element_size={this.state.element_size}/>
            )}
        />
      </div>
    );
  }
}

export default UserList;