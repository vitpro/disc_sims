import React, { Component } from 'react';
import ProgressBar from './ProgressBar';

export default class ProgressContainer extends Component {

    getProgressBarPercentage = () => {
        return (this.props.activeStep + 1) * 14;
    };

    render() {
        return (
            <div id="progressContainer">
                <div>
                    {this.props.steps.map((step, idx) => (
                        <span className="progressStep">{step}</span>
                    ))}

                </div>
                <ProgressBar completed={this.getProgressBarPercentage()} />
            </div>
        );
    }
}