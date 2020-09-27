import React, {Component} from 'react';

class Tab extends Component {

    onClick = () => {
        const {label, onClick, locked} = this.props;
        // if covenant hasn't been selected yet - should not be able to switch tabs
        if (locked) {
            return;
        }
        onClick(label);
    };

    render() {
        const {
            onClick,
            props: {
                activeTab,
                label,
            },
        } = this;

        let className = 'tab-list-item';

        if (activeTab === label) {
            className += ' tab-list-active';
        }

        return (
            <li
                className={className}
                onClick={onClick}
            >
                {label}
            </li>
        );
    }
}

export default Tab;