import React, { PureComponent } from 'react';
import {
  AppRegistry,
  StyleSheet,
  Text,
  View
} from 'react-native';

import { Main } from './src/components/Main';


class APP extends PureComponent {
  render() {
    return (
      <View>
        <Main />
      </View>
    );
  }
}


AppRegistry.registerComponent('loginer', () => APP);
