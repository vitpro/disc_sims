import React, { Component } from 'react';
import ProgressBar from './ProgressBar';

export default class ProgressContainer extends Component {

    getProgressBarPercentage = () => {
        const margins = 4;
        let progress = 0;
        for (let i = 0; i <= this.props.activeStep; i++) {
            progress += this.props.steps[i].length * 0.75 + margins;
        }
        return progress;
    };

    render() {
        return (
            <div id="progressContainer">
                <div>
                    {this.props.steps.map((step, idx) => (
                        <span className="progressStep" key={step}>{step}</span>
                    ))}

                </div>
                <ProgressBar completed={this.getProgressBarPercentage()} />
            </div>
        );
    }
}