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

import Create from './create'
import Tweet from './tweet'
import Authserver from './authserver'

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
            delete:false,
            timeoff:[]
        }
        this.handleDelete = this.handleDelete.bind(this)
        this.Auth = new Authserver()
        this.handleLogOut = this.handleLogOut.bind(this)
    }

    componentWillMount(){
        if(!this.Auth.loggedIn()){
            this.props.history.push('/')
        }else{
            axios.get('/api/getTable')
                    .then(res=>{
           console.log(res.data.value)
           this.setState({info: res.data.value})
       })
           axios.get('/api/getTimeOffTable')
                .then(res=>{
                    console.log(res.data.value)
                    this.setState({timeoff:res.data.value})
                }) 
        }
    }

   componentDidMount(){
        console.log(this.props)
        
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
   handleLogOut(){
    this.Auth.logout();
    this.props.history.push('/');
   }

   handleApprove(id,index){
        const info ={
            tiemStatus:1,
            timeoffID:id
        }
        axios.post('/api/acceptrequest',{info})
            .then(res=>{
                console.log(res.data)
               this.state.timeoff[index].timeStatus = 1
               this.forceUpdate()
            })
   }
   handleDecline(id,index){
    const info ={
        tiemStatus:0,
        timeoffID:id
    }
    axios.post('/api/rejectrequest',{info})
        .then(res=>{
            console.log(res.data)
            this.state.timeoff[index].timeStatus = 0
            this.forceUpdate()
        })
   }
    render() {
        const { classes } = this.props;
        return (
            <div style={{ marginTop: 40, marginLeft: 10, marginRight: 10 }}>
                <p>{(today.getMonth() + 1) + "/" + today.getDate() + "/" + today.getFullYear()}</p>
                <div style={{ textAlign: "right" }}>

                    <Popup trigger={<button style={{ boxShadow: '0 10px 20px -8px rgba(0, 0, 0,.7)' }}
                        className="btn btn-info btn-sm"> Add Employee</button>} modal>
                        <Create />
                    </Popup><br />

                    <button className="btn btn-primary btn-sm"
                        onClick={() => this.handleDelete()}
                        style={{ marginTop: 5, boxShadow: '0 10px 20px -8px rgba(0, 0, 0,.7)' }}>Delete Employee</button><br />

                    <Popup trigger={<button style={{ boxShadow: '0 10px 20px -8px rgba(0, 0, 0,.7)', marginTop: 5 }}
                        className="btn btn-info btn-sm"> Post a Tweet </button>} modal>
                        <Tweet />
                    </Popup><br />
                    <button className="btn btn-info btn-sm" style={{ marginTop: 5, boxShadow: '0 10px 20px -8px rgba(0, 0, 0,.7)' }} onClick={this.handleLogOut}>Log out</button>
                </div>

                <ul className="nav nav-tabs" id="myTab" role="tablist">
                    <li className="nav-item">
                        <a className="nav-link active" id="home-tab" data-toggle="tab" href="#employeeTable" role="tab"
                            aria-controls="employeeTable" aria-selected="true">EmployeeTable</a>
                    </li>
                    <li className="nav-item">
                        <a className="nav-link" id="profile-tab" data-toggle="tab" href="#vacationTable" role="tab"
                            aria-controls="vacationTable" aria-selected="false">VacationTable</a>
                    </li>
                </ul>
                <div className="tab-content" id="myTabContent">
                <div style={{ textAlign: 'center' }} className="tab-pane fade show active" id="employeeTable" role="tabpanel"
                                 aria-labelledby="employeeTable-tab">
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
                                                <button type="button" className="btn btn-danger btn-sm" onClick={() => this.deleteUser(row.userID)}> delete </button>
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

                    <div className="tab-pane fade" id="vacationTable" role="tabpanel"
                        aria-labelledby="vacationTable-tab">
                        <Table className={classes.table}>
                            <TableHead>
                                <TableRow>
                                <TableCell>Employee ID</TableCell>
                                <TableCell>StartDate</TableCell>
                                <TableCell>EndDate</TableCell>
                                <TableCell>timeStatus</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                            {this.state.timeoff.map((row,index) => {
                                return (
                                    <TableRow key={row.timeoffID}>
                                        <TableCell component="th" scope="row">{row.userID}</TableCell>
                                        <TableCell >{row.startDate}</TableCell>
                                        <TableCell >{row.endDate}</TableCell>
                                        <TableCell>{row.timeStatus == 2 ? 
                                            <div>
                                                <button className="btn btn-success btn-sm" onClick={()=>this.handleApprove(row.timeoffID,index)}>Approve</button>
                                                <button className="btn btn-danger btn-sm" onClick={()=>this.handleDecline(row.timeoffID,index)}>Decline</button>
                                            </div>
                                            : null}
                                                    {row.timeStatus == 1 ? <h5>Accept</h5>: null}
                                                    {row.timeStatus == 0 ? <h5>Decline</h5>: null}
                                        </TableCell>
                                    </TableRow>
                                );
                            })}
                            </TableBody>
                        </Table>
                    </div>
                </div>
            </div>
        );
    }
}

AdminTable.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(AdminTable)