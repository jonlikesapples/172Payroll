import React, { Component } from 'react';
import Authserver from './authserver';
import ApplyForVaction from './applyForVaction'
import Popup from "reactjs-popup";

import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Axios from 'axios';

const styles = theme => ({
    root: {
      width: 'auto',
      marginTop: theme.spacing.unit * 3,
    },
    table: {
        minWidth: 700,
    },
  });
  

const checkoutPanel = { background: '#FFFFFF', padding: '1rem', "borderRadius": "25px", border: '4px solid #c2c2c2', maxWidth: '70rem', marginLeft: "30px", marginBottom: "30px" }

class EmployeePage extends Component {
    constructor() {
        super()
        this.state = {
            name: "",
            userID: "",
            department: "",
            email: "",
            salary: '',
            hiredate: "",
            timeoff:[]
        }
        this.Auth = new Authserver()
        this.handleLogOut = this.handleLogOut.bind(this)
    }

    componentWillMount(){
        if(!this.Auth.loggedIn()){
            this.props.history.push('/')
        }
        else{
        const userID = this.props.location.state.info.userID
        this.setState(this.props.location.state.info)
        Axios.get('/api/oneUserTimeOff',{params:{userID}})
            .then(res=>{
                console.log(res.data)
                this.setState({timeoff:res.data.value})
            })
        }
    }

    handleLogOut() {
        this.Auth.logout();
        this.props.history.push('/');
    }

    render() {
        const { classes } = this.props;
        return (
            <div style={{ marginTop: 80 }} >
                <ul className="nav nav-tabs" id="myTab" role="tablist">
                    <li className="nav-item">
                        <a className="nav-link active" id="home-tab" data-toggle="tab" href="#employeeinfo" role="tab"
                            aria-controls="employeeinfo" aria-selected="true">Employee Info</a>
                    </li>
                    <li className="nav-item">
                        <a className="nav-link" id="profile-tab" data-toggle="tab" href="#vacationTable" role="tab"
                            aria-controls="vacationTable" aria-selected="false">Vacation History</a>
                    </li>
                </ul>
                <div className="tab-content" id="myTabContent">
                    <div style={{ textAlign: 'center' }} className="tab-pane fade show active" id="employeeinfo" role="tabpanel"
                        aria-labelledby="employeeinfo-tab">
                        <div style={checkoutPanel}>
                            <form>
                                <div className="form-group">
                                    <div className="form-row">
                                        <div className="form-group col-md-6">
                                            <label htmlFor="inputName" className="control-label">
                                                Name
                                        </label>
                                            <h3>  {this.state.name} </h3>
                                        </div>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <div className="form-group">
                                        <label htmlFor="inputEmail">Employee ID</label>
                                        <h3>{this.state.userID} </h3>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <div className="form-group">
                                        <label htmlFor="inputAddress">Department </label>
                                        <h3>{this.state.department}</h3>
                                    </div>
                                </div>
                                <div className="form-row">
                                    <div className="form-group col-md-6">
                                        <label htmlFor="inputCity">Salary </label>
                                        <h3>{this.state.salary}</h3>
                                    </div>
                                    <div className="form-group col-md-4">
                                        <label htmlFor="inputState">Email</label>
                                        <h3>{this.state.email}</h3>
                                    </div>
                                    <div className="form-group col-md-2">
                                        <label htmlFor="inputZip">Hired Date</label>
                                        <h3>{this.state.hireDate}</h3>
                                    </div>
                                </div>
                            </form>
                        </div>
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
                            {this.state.timeoff.map(row => {
                                return (
                                    <TableRow key={row.timeoffID}>
                                        <TableCell component="th" scope="row">{row.userID}</TableCell>
                                        <TableCell >{row.startDate}</TableCell>
                                        <TableCell >{row.endDate}</TableCell>
                                        <TableCell>{row.timeStatus == 2 ? 
                                            <h5>Pending</h5>
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
                <button className="btn btn-info btn-sm" style={{ marginLeft: 40, marginTop: 5, boxShadow: '0 10px 20px -8px rgba(0, 0, 0,.7)' }} onClick={this.handleLogOut}>Log out</button>

                <Popup trigger={<button style={{ boxShadow: '0 10px 20px -8px rgba(0, 0, 0,.7)', marginLeft: 50, marginTop: 5 }}
                    className="btn btn-info btn-sm">Apply for Holiday</button>} modal
                    contentStyle={{ width: "200px", height: "200px" }}>
                    <ApplyForVaction userID={this.state.userID} />
                </Popup><br />
            </div>
            </div>
        );
    }
}

EmployeePage.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(EmployeePage)