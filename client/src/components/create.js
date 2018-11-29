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
    onChange = ({ target: { name, value } }) => {
        this.setState({ [name]: value })
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
        <div className="login_container" style={{margin:"25%"}}>
        <div style ={{border:"1px solid #c2c2c2",textAlign: "center"}}>
        <form onSubmit={this.submitLogin}>
            <h2>Add you info</h2>
            <div className="form_element">
                <input 
                    type="text"
                    placeholder="Enter your lastname"
                    name='lastname'
                    value={this.state.lastname}
                    onChange={this.onChange}
                />
            </div>
            <div className="form_element">
                <input 
                    type="text"
                    placeholder="Enter your firstname"
                    name='firstname'
                    value={this.state.firstname}
                    onChange={this.onChange}
                />
            </div>
            <div className="form_element">
                <input 
                    type="number"
                    name='salary'
                    placeholder="Enter your salary"
                    value={this.state.salary}
                    onChange={this.onChange}
                />
            </div>
            <button type="submit">Add</button>
            </form>
            </div>
            </div>
    );
}   
}

export default Create;