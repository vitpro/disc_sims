import React, { Component } from 'react';
import ProgressBar from './ProgressBar';

export default class ProgressContainer extends Component {
    render() {
        return (
            <div id="progressContainer">
                <div>
                    <span className="progressStep">1. Character Details</span>
                    <span className="progressStep">2. Sim Options</span>
                </div>
                <ProgressBar completed={this.props.barCompleted} displayPercentage={this.props.barDisplayPercentage} />
            </div>
        );
    }
}