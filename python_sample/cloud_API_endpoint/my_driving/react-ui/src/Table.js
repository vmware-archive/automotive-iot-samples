import React, { Component } from "react";
import ReactTable from "react-table";
import "react-table/react-table.css";
import axios from "axios";

class Table extends Component {
  constructor() {
    super();
    this.state = {
      data: []
    };
  }

  componentDidMount() {
    // TODO: IP and port from config file?
    axios.get("http://0.0.0.0:3001/events").then(res => {
      const data = res.data;
      this.setState({data});
    });
  }

  convertDate(timestamp){
    const date = new Date(timestamp* 1000);
    return date.toISOString();
  }
  
  render() {
    const { data } = this.state;
    const columns = [
      {
        Header: "Client ID",
        accessor: "client_side_id" // String-based value accessors!
      },
      {
        Header: "Client Name",
        accessor: "user" // String-based value accessors!
      },
      {
        Header: "Time",
        accessor: "event_timestamp",
        Cell: props => <span>{this.convertDate(props.value)}</span> // Custom cell components!
      },
      {
        Header: "Distance",
        accessor: "distance"
      },
      {
        Header: "Fuel",
        accessor: "fuel"
      }
    ];
    return (
      <ReactTable 
        data={data} 
        columns={columns} 
        defaultPageSize={10}
        className="-striped -highlight"/>
    );
  }
}

export default Table;
