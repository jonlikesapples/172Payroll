import React, { Component } from 'react';

const checkoutPanel = { background: '#FFFFFF', marginBottom: '0', padding: '1rem', "borderRadius": "25px", border: '4px solid #c2c2c2', maxWidth: '70rem', marginLeft: "30px", marginBottom: "30px" }

class EmployeePage extends Component {
    constructor() {
        super()
        this.state = {
            name: "TestBoy",
            userID: "cd54b4ddb7813d2d95813fa99e35950a53bf100d8ef87f224637c011f5bf37b8",
            department: "testing",
            email: "testing@test.com",
            salary: 100000000,
            hiredate: "11/1/2018"
        }
    }

    render() {
        return (
            <div style={{marginTop:80}} >
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
                            <h3>{this.state.hiredate}</h3>
                        </div>
                    </div>
                </form>
                </div>
            </div>
        );
    }
}

export default EmployeePage;