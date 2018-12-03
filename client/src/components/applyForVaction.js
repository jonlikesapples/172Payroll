import React, { Component } from 'react';



class ApplyForVaction extends Component {
    constructor(props){
        super(props)
        this.state ={
            startDate:'',
            endDate:'',
            userID:props.userID
        }
        this.submitForm = this.submitForm.bind(this)
    }

    onChange = ({ target: { name, value } }) => {
        this.setState({ [name]: value })
    }

    submitForm(e){
        e.preventDefault();
        console.log(this.state)
    }

    render() {
        return (
            <div>
                <form onSubmit={this.submitForm}>
                <div className="form_element">
                Start Date
                <input 
                    type="date"
                    name='startDate'
                    placeholder="mm/dd/yyyy"
                    value={this.state.hireDate}
                    onChange={this.onChange}
                />
                </div>
                <div className="form_element">
                End Date
                <input 
                    type="date"
                    name='endDate'
                    placeholder="mm/dd/yyyy"
                    value={this.state.hireDate}
                    onChange={this.onChange}
                />
                </div>
                <button type="submit" className="btn btn-info btn-sm">Submit</button>
                </form>
            </div>
        );
    }
}

export default ApplyForVaction;