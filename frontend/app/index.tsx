import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Animated,
  Platform,
  StatusBar,
  TextInput,
  Keyboard,
  KeyboardAvoidingView,
  Pressable,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import Constants from 'expo-constants';

const BACKEND_URL = Constants.expoConfig?.extra?.EXPO_PUBLIC_BACKEND_URL || process.env.EXPO_PUBLIC_BACKEND_URL;

interface RandomNumberResponse {
  number: number;
  category: string;
  seed_used: number;
}

export default function Home() {
  const [randomNumber, setRandomNumber] = useState<number | null>(null);
  const [category, setCategory] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [scaleAnim] = useState(new Animated.Value(0));
  const [periodNumber, setPeriodNumber] = useState<string>('');

  const generateNumber = async () => {
    setLoading(true);
    setError('');
    
    try {
      // Validate period number input (required for identification only)
      if (periodNumber.trim() === '') {
        setError('Please enter a period number');
        setLoading(false);
        return;
      }
      
      const parsedPeriod = parseInt(periodNumber.trim(), 10);
      if (isNaN(parsedPeriod) || parsedPeriod <= 0) {
        setError('Please enter a valid period number (positive integer)');
        setLoading(false);
        return;
      }
      
      // Generate random seed automatically (NOT using period number)
      // Seed is auto-generated from timestamp for randomness
      const requestBody = {}; // Empty body means auto-generate seed

      const response = await fetch(`${BACKEND_URL}/api/generate-random`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error('Failed to generate random number');
      }

      const data: RandomNumberResponse = await response.json();
      
      // Reset animation
      scaleAnim.setValue(0);
      
      // Update state
      setRandomNumber(data.number);
      setCategory(data.category);
      
      // Animate the number appearance
      Animated.spring(scaleAnim, {
        toValue: 1,
        friction: 4,
        tension: 40,
        useNativeDriver: true,
      }).start();
      
    } catch (err) {
      setError('Failed to generate number. Please try again.');
      console.error('Error generating number:', err);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryColor = () => {
    // Color based on number: Even (0,2,4,6,8) = Red, Odd (1,3,5,7,9) = Green
    if (randomNumber !== null) {
      if (randomNumber % 2 === 0) {
        return '#F44336'; // Red for even numbers
      } else {
        return '#4CAF50'; // Green for odd numbers
      }
    }
    return '#757575';
  };

  const getCategoryBackgroundColor = () => {
    // Background color based on number: Even = Light Red, Odd = Light Green
    if (randomNumber !== null) {
      if (randomNumber % 2 === 0) {
        return '#FFEBEE'; // Light red for even numbers
      } else {
        return '#E8F5E9'; // Light green for odd numbers
      }
    }
    return '#F5F5F5';
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="dark-content" backgroundColor="#FFFFFF" />
      <KeyboardAvoidingView 
        style={styles.flex}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      >
        <Pressable style={styles.flex} onPress={Keyboard.dismiss}>
          <View style={styles.container}>
            {/* Header */}
            <View style={styles.header}>
              <Text style={styles.title}>Random Number Generator</Text>
              <Text style={styles.subtitle}>@OJAS GAMBEERA</Text>
            </View>

            {/* Period Number Input */}
            <View style={styles.seedInputContainer}>
              <Text style={styles.seedLabel}>Enter Period Number</Text>
              <TextInput
                style={styles.seedInput}
                value={periodNumber}
                onChangeText={(text) => {
                  // Only allow numbers
                  const numericText = text.replace(/[^0-9]/g, '');
                  setPeriodNumber(numericText);
                  // Clear results when period number is cleared
                  if (numericText.trim() === '') {
                    setRandomNumber(null);
                    setCategory('');
                  }
                }}
                placeholder="Enter period number"
                placeholderTextColor="#999999"
                keyboardType="number-pad"
                returnKeyType="done"
                editable={!loading}
                autoCapitalize="none"
                autoCorrect={false}
                autoComplete="off"
                selectTextOnFocus={true}
                maxLength={10}
                onSubmitEditing={() => {
                  Keyboard.dismiss();
                  if (periodNumber.trim() !== '') {
                    generateNumber();
                  }
                }}
              />
              <Text style={styles.noteText}>Note: Please enter last 3 digit number</Text>
            </View>

            {/* Main Display Area */}
            <View style={styles.displayContainer}>
          {randomNumber !== null ? (
            <Animated.View 
              style={[
                styles.resultContainer,
                { 
                  backgroundColor: getCategoryBackgroundColor(),
                  transform: [{ scale: scaleAnim }]
                }
              ]}
            >
              <Text style={[styles.categoryDisplayText, { color: getCategoryColor() }]}>
                {category}
              </Text>
            </Animated.View>
          ) : (
            <View style={styles.placeholderContainer}>
              <Text style={styles.placeholderText}>?
              </Text>
              <Text style={styles.instructionText}>Tap Generate to see Big or Small</Text>
            </View>
          )}
        </View>

        {/* Error Message */}
        {error ? (
          <View style={styles.errorContainer}>
            <Text style={styles.errorText}>{error}</Text>
          </View>
        ) : null}

        {/* Info Box */}
        <View style={styles.infoBox}>
          <Text style={styles.infoTitle}>How it works:</Text>
          <Text style={styles.infoText}>• Numbers 0-4 are categorized as "Small"</Text>
          <Text style={styles.infoText}>• Numbers 5-9 are categorized as "Big"</Text>
          <Text style={styles.infoText}>• Uses PRNG Linear Congruential Generator</Text>
        </View>

        {/* Generate Button */}
        <TouchableOpacity
          style={[styles.generateButton, loading && styles.generateButtonDisabled]}
          onPress={generateNumber}
          disabled={loading}
          activeOpacity={0.7}
        >
          {loading ? (
            <ActivityIndicator color="#FFFFFF" size="small" />
          ) : (
            <Text style={styles.generateButtonText}>Generate</Text>
          )}
        </TouchableOpacity>

        {/* Watermark */}
        <View style={styles.watermarkContainer}>
          <Text style={styles.watermarkText}>Developed by OJAS GAMBEERA</Text>
        </View>
          </View>
        </Pressable>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  flex: {
    flex: 1,
  },
  container: {
    flex: 1,
    paddingHorizontal: 24,
    paddingVertical: 16,
    backgroundColor: '#FFFFFF',
  },
  header: {
    alignItems: 'center',
    marginBottom: 24,
    marginTop: 8,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1A1A1A',
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 14,
    color: '#666666',
    textAlign: 'center',
  },
  seedInputContainer: {
    marginBottom: 16,
  },
  seedLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1A1A1A',
    marginBottom: 8,
  },
  seedInput: {
    backgroundColor: '#FFFFFF',
    borderWidth: 2,
    borderColor: '#2196F3',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 16,
    fontSize: 18,
    color: '#1A1A1A',
    minHeight: 56,
    textAlign: 'center',
    fontWeight: '600',
  },
  noteText: {
    fontSize: 13,
    color: '#666666',
    marginTop: 8,
    fontStyle: 'italic',
  },
  displayContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 24,
  },
  resultContainer: {
    width: 280,
    height: 280,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.15,
        shadowRadius: 12,
      },
      android: {
        elevation: 8,
      },
    }),
  },
  categoryDisplayText: {
    fontSize: 72,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  placeholderContainer: {
    alignItems: 'center',
  },
  placeholderText: {
    fontSize: 120,
    color: '#E0E0E0',
    fontWeight: 'bold',
  },
  instructionText: {
    fontSize: 16,
    color: '#999999',
    marginTop: 16,
    textAlign: 'center',
  },
  errorContainer: {
    backgroundColor: '#FFEBEE',
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
  },
  errorText: {
    color: '#C62828',
    fontSize: 14,
    textAlign: 'center',
  },
  infoBox: {
    backgroundColor: '#F5F5F5',
    padding: 16,
    borderRadius: 12,
    marginBottom: 24,
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1A1A1A',
    marginBottom: 8,
  },
  infoText: {
    fontSize: 14,
    color: '#666666',
    marginBottom: 4,
    lineHeight: 20,
  },
  generateButton: {
    backgroundColor: '#2196F3',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 56,
    ...Platform.select({
      ios: {
        shadowColor: '#2196F3',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
      },
      android: {
        elevation: 4,
      },
    }),
  },
  generateButtonDisabled: {
    backgroundColor: '#B0BEC5',
  },
  generateButtonText: {
    fontSize: 20,
    fontWeight: '600',
    color: '#FFFFFF',
  },
  watermarkContainer: {
    marginTop: 16,
    alignItems: 'center',
  },
  watermarkText: {
    fontSize: 12,
    color: '#999999',
    fontStyle: 'italic',
  },
});