import React, {Component} from 'react';
import Tab from './Tab';

class Tabs extends Component {

    constructor(props) {
        super(props);

        this.state = {
            activeTab: this.props.children[0].props.label,
        };
    }

    onClickTabItem = (tab) => {
        this.setState({activeTab: tab});
    };

    render() {
        const {
            onClickTabItem,
            props: {
                children,
                listId,
            },
            state: {
                activeTab,
            }
        } = this;

        return (
            <div className="tabs">
                <ol className="tab-list" id={listId}>
                    {children.map((child) => {
                        const {label, locked} = child.props;

                        return (
                            <Tab
                                activeTab={activeTab}
                                key={label}
                                label={label}
                                onClick={onClickTabItem}
                                locked={locked}
                            />
                        );
                    })}
                </ol>
                <div className="tab-content">
                    {children.map((child) => {
                        if (child.props.label !== activeTab) return undefined;
                        return child.props.children;
                    })}
                </div>
            </div>
        );
    }
}

export default Tabs;