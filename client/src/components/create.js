import React, { Component } from 'react';
import axios from 'axios';

class Create extends Component {

    constructor(props) {
		super(props)
		this.state = {
            firstname:'',
            lastname:'',
            salary:''
        }
        this.submitLogin = this.submitLogin.bind(this)
        //this.Auth = new Authserver();
	}

    
    ////////////////Login ////////////////////
    handleInputFirstname = (event) => {
        this.setState({firstname:event.target.value})
    }
    handleInputLastname = (event) => {
        this.setState({lastname:event.target.value})
    }

    handleInputSalary = (event) => {
        this.setState({salary:event.target.value})
    }

    submitLogin = (e) =>{
        e.preventDefault();
        let firstname = this.state.firstname;
        let lastname = this.state.lastname;
        let salary = this.state.salary;
        axios.post(`/api/create?firstname=${firstname}&lastname=${lastname}&salary=${salary}`)
            .then(res=>{   
                console.log(res.data)
            })

    }

    updateForm = (newState) =>{
        this.setState({
            State:newState
        })
    }
    

render(){
    return (    
        <div>
        <div className="login_container" style ={{border:"1px solid #c2c2c2",width:"50%",margin:"auto"}}>
        <form onSubmit={this.submitLogin}>
            <h2>Log in here</h2>
            <div className="form_element">
                <input 
                    type="text"
                    placeholder="Enter your lastname"
                    value={this.state.lastname}
                    onChange={this.handleInputLastname}
                />
            </div>
            <div className="form_element">
                <input 
                    type="text"
                    placeholder="Enter your firstname"
                    value={this.state.firstname}
                    onChange={this.handleInputFirstname}
                />
            </div>
            <div className="form_element">
                <input 
                    type="number"
                    placeholder="Enter your salary"
                    value={this.state.salary}
                    onChange={this.handleInputSalary}
                />
            </div>
            <button type="submit">Log in</button>
            </form>
            </div>
            </div>
    );
}   
}

export default Create;