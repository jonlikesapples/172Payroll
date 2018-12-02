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
import Tweet from './tweet'

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
            info:[],
            delete:false
        }
        this.handleDelete = this.handleDelete.bind(this)
    }

   componentDidMount(){
       axios.get('/api/getTable')
       .then(res=>{
           console.log(res.data.value)
           res.data.value.forEach(element => {
               element.select = false;
           });
           this.setState({info: res.data.value})
       })
   }

   handleDelete(){
       this.setState({delete:!this.state.delete})
   }

   deleteUser(id){
       axios.delete('/api/delete',{data: {id: id}})
            .then(res=> {
                console.log(res.data)
                window.location.reload()
            })
   }

    render() {
        console.log(this.state)
        const { classes } = this.props;
        return (
        <div style={{marginTop:40,marginLeft:10,marginRight:10}}>
            <p>{  (today.getMonth()+1) + "/" + today.getDate() + "/" + today.getFullYear()}</p>
            <div style={{textAlign:"right"}}>

            <Popup trigger={<button style={{boxShadow:'0 10px 20px -8px rgba(0, 0, 0,.7)'}} 
            className="btn btn-info btn-sm"> Add Employee</button>} modal>
                <Create />
            </Popup><br/>

                <button className="btn btn-primary btn-sm"
                onClick={()=>this.handleDelete()} 
                style={{marginTop:5,boxShadow:'0 10px 20px -8px rgba(0, 0, 0,.7)'}}>Delete Employee</button><br/>

            <Popup trigger={<button style={{boxShadow:'0 10px 20px -8px rgba(0, 0, 0,.7)',marginTop:5}} 
            className="btn btn-info btn-sm"> Post a Tweet </button>} modal>
                <Tweet />
            </Popup><br/>
            
            </div>
            <div style={{textAlign:'center'}}>
            <Table className={classes.table}>
              <TableHead>
                <TableRow>
                    {this.state.delete ?  
                    <TableCell>
                    </TableCell>
                 : null}
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
                    
                    {this.state.delete ? 
                    <TableCell> 
                        <button type="button" className="btn btn-danger btn-sm" onClick={()=>this.deleteUser(row.userID)}> delete </button>
                    </TableCell>
                    : null}  
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