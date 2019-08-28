import React, { Component } from 'react';
import Table from "./Table";
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h2>Smart City</h2>
        </header>
        <div className="App-body">
          <Table/>
        </div>
      </div>
    );
  }
}

export default App;
