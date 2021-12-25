import React, { Component } from "react";
import Avatar, { genConfig } from 'react-nice-avatar';
import axios from "axios";

function NFT() {
  const config = genConfig({
    isGradient:true,
  });
  return (
    <Avatar
      style={{ width: "8rem", height: "8rem" }}
      {...config}
    />
  );
}

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      viewCompleted: false,
      activeItem: {
        user: "",
        bio: "",
        location: "",
        picture: ""
      },
      userProfile: []
      };
  }

  async componentDidMount() {
      try {
        const res = await fetch('http://localhost:8000/accounts/api/userprofile/');
        const userProfile = await res.json();
        this.setState({
          userProfile
        });
      } catch (e) {
        console.log(e);
    }
  }

  renderItems = () => {
      const { viewCompleted } = this.state;
      const newItems = this.state.userProfile
      return newItems.map(item => (
        <li
          className="list-group-item d-flex justify-content-between align-items-center p-3"
        >
        <div className="App">
            <NFT />
        </div>
          <span>
              User {item.user} <br/>
              {item.bio} <br/>
              {item.location} <br/>
              {item.picture} <br/>
            </span>
            <br/>
        </li>
      ));
    };

  render() {
      return (
        <main className="content">
        <h1 className="text-center">Gen React Avatars</h1>
          <div className="row">
            <div className="col-md-6 col-sm-10 mx-auto p-0">
              <div className="card p-0">
                <ul className="list-group list-group-flush">
                  {this.renderItems()}
                </ul>
              </div>
            </div>
          </div>
        </main>
      );
    }
}

export default App;
