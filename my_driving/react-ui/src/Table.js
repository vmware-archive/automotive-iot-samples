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
    axios.get("http://0.0.0.0:2000/events").then(res => {
      const data = res.data;
      this.setState({data});
    });
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
        Header: "Type",
        accessor: "event_type"
        // Cell: props => <span className='number'>{props.value}</span> // Custom cell components!
      },
      {
        Header: "Time",
        accessor: "event_timestamp"
      },
      {
        Header: "Location",
        accessor: "gps_coord"
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
