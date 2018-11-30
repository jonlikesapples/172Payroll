import React, { Component } from 'react';
import Popup from "reactjs-popup";
import axios from 'axios';

import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import Create from './create'

const styles = theme => ({
    root: {
      width: 'auto',
      marginTop: theme.spacing.unit * 3,
    },
    table: {
        minWidth: 700,
    },
  });
  
  
  ////////////switch with state when backend ready


  const today = new Date()

class AdminTable extends Component {
    constructor(){
        super()
        this.state={
            info:[]
        }
    }

   componentDidMount(){
       axios.get('/api/getTable')
       .then(res=>{
           var obj =[];
           for(var i = 0; i < res.data.length;i++){
                var item = JSON.parse(res.data[i])
                obj.push(item)
           }

           this.setState({info: obj})
       })
   }

    render() {
        console.log(this.state.info)
        const { classes } = this.props;
        return (
        <div className="container" style={{marginTop:40}}>
            <p>{  (today.getMonth()+1) + "/" + today.getDate() + "/" + today.getFullYear()}</p>
            <div style={{textAlign:"right"}}>
            <Popup trigger={<button style={{boxShadow:'0 10px 20px -8px rgba(0, 0, 0,.7)'}} 
            className="btn btn-info btn-sm"> Add Employee</button>} modal>
                <Create />
            </Popup><br/>
                <button className="btn btn-primary btn-sm" style={{marginTop:5}}>Delete Employee</button>
            </div>
            <div style={{textAlign:'center'}}>
            <Table className={classes.table}>
              <TableHead>
                <TableRow>
                  <TableCell>Employee Name</TableCell>
                  <TableCell numeric>Employee ID</TableCell>
                  <TableCell >Hired Date</TableCell>
                  <TableCell>Department</TableCell>
                  <TableCell numeric>Salary</TableCell>
                  <TableCell>Email</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {this.state.info.map(row => {
                  return (
                    <TableRow key={row.userID}>
                      <TableCell component="th" scope="row">
                        {row.name}
                      </TableCell>
                      <TableCell numeric>{row.userID}</TableCell>
                      <TableCell >{row.hireDate}</TableCell>
                      <TableCell >{row.department}</TableCell>
                      <TableCell numeric>{row.salary}</TableCell>
                      <TableCell>{row.email}</TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
            </div>
        </div>
        );
    }
}

AdminTable.propTypes = {
    classes: PropTypes.object.isRequired,
  };
  
  export default withStyles(styles)(AdminTable)