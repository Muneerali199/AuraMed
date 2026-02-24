import React, { useState } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, ScrollView, TextInput, Alert, ActivityIndicator } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

const API_BASE = 'http://10.0.2.2:5000/api';

function HomeScreen({ navigation }: any) {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>🏥 AuraMed</Text>
        <Text style={styles.subtitle}>Clinical AI Assistant</Text>
        <Text style={styles.status}>● Offline Mode</Text>
      </View>
      
      <View style={styles.menuContainer}>
        <TouchableOpacity 
          style={styles.menuItem} 
          onPress={() => navigation.navigate('VoiceRecord')}
        >
          <Text style={styles.menuIcon}>🎤</Text>
          <View>
            <Text style={styles.menuTitle}>Voice Recording</Text>
            <Text style={styles.menuDesc}>Record clinical notes</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.menuItem}
          onPress={() => navigation.navigate('PatientData')}
        >
          <Text style={styles.menuIcon}>📋</Text>
          <View>
            <Text style={styles.menuTitle}>Patient Data</Text>
            <Text style={styles.menuDesc}>Enter patient information</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.menuItem}
          onPress={() => navigation.navigate('DrugInteractions')}
        >
          <Text style={styles.menuIcon}>💊</Text>
          <View>
            <Text style={styles.menuTitle}>Drug Interactions</Text>
            <Text style={styles.menuDesc}>Check medication safety</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.menuItem}
          onPress={() => navigation.navigate('Results')}
        >
          <Text style={styles.menuIcon}>📊</Text>
          <View>
            <Text style={styles.menuTitle}>Results</Text>
            <Text style={styles.menuDesc}>View analysis results</Text>
          </View>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

function VoiceRecordScreen({ navigation }: any) {
  const [recording, setRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const simulateRecording = () => {
    setRecording(true);
    setTimeout(() => {
      setRecording(false);
      setTranscript('Patient reports fatigue, chest discomfort, and shortness of breath. History of hypertension and diabetes.');
    }, 2000);
  };

  const analyzeTranscript = async () => {
    if (!transcript) {
      Alert.alert('Error', 'Please enter or record a transcript');
      return;
    }
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/analyze-voice`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      Alert.alert('Error', 'Failed to connect to server. Make sure the Python server is running.');
    }
    setLoading(false);
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.screenContainer}>
        <Text style={styles.screenTitle}>🎤 Voice Recording</Text>
        
        <TouchableOpacity 
          style={[styles.recordButton, recording && styles.recordButtonActive]}
          onPress={simulateRecording}
        >
          <Text style={styles.recordButtonText}>
            {recording ? 'Recording...' : 'Tap to Record'}
          </Text>
        </TouchableOpacity>

        <Text style={styles.label}>Transcript:</Text>
        <TextInput
          style={styles.textArea}
          multiline
          numberOfLines={5}
          value={transcript}
          onChangeText={setTranscript}
          placeholder="Enter or record clinical transcript..."
        />

        <TouchableOpacity 
          style={styles.primaryButton}
          onPress={analyzeTranscript}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.primaryButtonText}>Analyze Transcript</Text>
          )}
        </TouchableOpacity>

        {result && (
          <View style={styles.resultContainer}>
            <Text style={styles.resultTitle}>Analysis Results</Text>
            <Text style={styles.resultText}>Symptoms: {result.symptoms_detected?.join(', ') || 'None'}</Text>
            <Text style={styles.resultText}>SOAP Notes:</Text>
            <Text style={styles.soapText}>S: {result.soap_notes?.subjective}</Text>
            <Text style={styles.soapText}>O: {result.soap_notes?.objective}</Text>
            <Text style={styles.soapText}>A: {result.soap_notes?.assessment}</Text>
            <Text style={styles.soapText}>P: {result.soap_notes?.plan}</Text>
          </View>
        )}
      </View>
    </ScrollView>
  );
}

function PatientDataScreen({ navigation }: any) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [patientData, setPatientData] = useState({
    congestive_heart_failure: false,
    hypertension: false,
    age_75_plus: false,
    diabetes: false,
    stroke_tia: false,
  });

  const calculateScore = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/chads2-score`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(patientData),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      Alert.alert('Error', 'Failed to connect to server');
    }
    setLoading(false);
  };

  const toggleField = (field: string) => {
    setPatientData(prev => ({ ...prev, [field]: !prev[field as keyof typeof prev] }));
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.screenContainer}>
        <Text style={styles.screenTitle}>📋 Patient Data</Text>
        <Text style={styles.subLabel}>CHADS2 Score Calculator</Text>

        <View style={styles.checkboxContainer}>
          {[
            { key: 'congestive_heart_failure', label: 'Congestive Heart Failure' },
            { key: 'hypertension', label: 'Hypertension' },
            { key: 'age_75_plus', label: 'Age ≥ 75' },
            { key: 'diabetes', label: 'Diabetes' },
            { key: 'stroke_tia', label: 'Prior Stroke/TIA' },
          ].map(item => (
            <TouchableOpacity 
              key={item.key} 
              style={styles.checkboxItem}
              onPress={() => toggleField(item.key)}
            >
              <View style={[
                styles.checkbox,
                patientData[item.key as keyof typeof patientData] && styles.checkboxChecked
              ]}>
                {patientData[item.key as keyof typeof patientData] && <Text>✓</Text>}
              </View>
              <Text style={styles.checkboxLabel}>{item.label}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <TouchableOpacity 
          style={styles.primaryButton}
          onPress={calculateScore}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.primaryButtonText}>Calculate Score</Text>
          )}
        </TouchableOpacity>

        {result && (
          <View style={styles.resultContainer}>
            <Text style={styles.resultTitle}>CHADS2 Score</Text>
            <Text style={styles.scoreDisplay}>{result.score} / {result.max_score}</Text>
            <Text style={styles.riskLevel}>Risk Level: {result.risk_level}</Text>
            <Text style={styles.resultText}>Components:</Text>
            {result.components?.map((comp: string, i: number) => (
              <Text key={i} style={styles.componentText}>• {comp}</Text>
            ))}
          </View>
        )}
      </View>
    </ScrollView>
  );
}

function DrugInteractionsScreen({ navigation }: any) {
  const [medications, setMedications] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const checkInteractions = async () => {
    if (!medications.trim()) {
      Alert.alert('Error', 'Please enter medications');
      return;
    }
    setLoading(true);
    try {
      const medsList = medications.split(',').map(m => m.trim()).filter(m => m);
      const response = await fetch(`${API_BASE}/drug-interactions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ medications: medsList }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      Alert.alert('Error', 'Failed to connect to server');
    }
    setLoading(false);
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.screenContainer}>
        <Text style={styles.screenTitle}>💊 Drug Interactions</Text>
        
        <Text style={styles.label}>Enter medications (comma separated):</Text>
        <TextInput
          style={styles.textArea}
          multiline
          numberOfLines={3}
          value={medications}
          onChangeText={setMedications}
          placeholder="e.g., Warfarin, Aspirin, Ibuprofen"
        />

        <TouchableOpacity 
          style={styles.primaryButton}
          onPress={checkInteractions}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.primaryButtonText}>Check Interactions</Text>
          )}
        </TouchableOpacity>

        {result && (
          <View style={styles.resultContainer}>
            <Text style={styles.resultTitle}>Drug Interaction Report</Text>
            <Text style={styles.resultText}>Medications: {result.medications?.join(', ')}</Text>
            <Text style={styles.resultText}>Interactions Found: {result.count}</Text>
            
            {result.interactions?.map((inter: any, i: number) => (
              <View key={i} style={styles.interactionCard}>
                <Text style={styles.interactionDrugs}>{inter.drugs?.join(' + ')}</Text>
                <Text style={styles.interactionText}>{inter.interaction}</Text>
                <Text style={[styles.severity, inter.severity === 'High' && styles.severityHigh]}>
                  Severity: {inter.severity}
                </Text>
              </View>
            ))}
            
            {result.count === 0 && (
              <Text style={styles.noInteractions}>No known interactions found</Text>
            )}
          </View>
        )}
      </View>
    </ScrollView>
  );
}

function ResultsScreen({ navigation }: any) {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.screenContainer}>
        <Text style={styles.screenTitle}>📊 Results</Text>
        
        <View style={styles.resultContainer}>
          <Text style={styles.resultTitle}>Recent Analyses</Text>
          <Text style={styles.noData}>No recent results</Text>
          <Text style={styles.hint}>Use the Voice Recording or Patient Data screens to perform analyses</Text>
        </View>

        <View style={styles.infoCard}>
          <Text style={styles.infoTitle}>ℹ️ About AuraMed</Text>
          <Text style={styles.infoText}>
            AuraMed is a privacy-preserving, offline-first clinical workflow assistant.
            All data is processed locally on your device.
          </Text>
        </View>
      </View>
    </ScrollView>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} options={{ headerShown: false }} />
        <Stack.Screen name="VoiceRecord" component={VoiceRecordScreen} options={{ title: 'Voice Recording' }} />
        <Stack.Screen name="PatientData" component={PatientDataScreen} options={{ title: 'Patient Data' }} />
        <Stack.Screen name="DrugInteractions" component={DrugInteractionsScreen} options={{ title: 'Drug Interactions' }} />
        <Stack.Screen name="Results" component={ResultsScreen} options={{ title: 'Results' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#2563eb',
    padding: 30,
    alignItems: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
  },
  subtitle: {
    fontSize: 16,
    color: '#e0e7ff',
    marginTop: 5,
  },
  status: {
    fontSize: 14,
    color: '#86efac',
    marginTop: 10,
  },
  menuContainer: {
    padding: 15,
  },
  menuItem: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  menuIcon: {
    fontSize: 32,
    marginRight: 15,
  },
  menuTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1f2937',
  },
  menuDesc: {
    fontSize: 14,
    color: '#6b7280',
    marginTop: 2,
  },
  screenContainer: {
    padding: 20,
  },
  screenTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 20,
  },
  subLabel: {
    fontSize: 14,
    color: '#6b7280',
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 8,
  },
  textArea: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    minHeight: 100,
    borderWidth: 1,
    borderColor: '#d1d5db',
    marginBottom: 15,
  },
  recordButton: {
    backgroundColor: '#ef4444',
    borderRadius: 60,
    width: 120,
    height: 120,
    alignSelf: 'center',
    justifyContent: 'center',
    marginBottom: 20,
  },
  recordButtonActive: {
    backgroundColor: '#dc2626',
  },
  recordButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
  },
  primaryButton: {
    backgroundColor: '#2563eb',
    borderRadius: 8,
    padding: 15,
    alignItems: 'center',
    marginTop: 10,
  },
  primaryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  checkboxContainer: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 15,
    marginBottom: 15,
  },
  checkboxItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 4,
    borderWidth: 2,
    borderColor: '#2563eb',
    marginRight: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  checkboxChecked: {
    backgroundColor: '#2563eb',
  },
  checkboxLabel: {
    fontSize: 16,
    color: '#374151',
  },
  resultContainer: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    marginTop: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  resultTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 10,
  },
  resultText: {
    fontSize: 14,
    color: '#4b5563',
    marginBottom: 5,
  },
  scoreDisplay: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#2563eb',
    textAlign: 'center',
    marginVertical: 10,
  },
  riskLevel: {
    fontSize: 18,
    fontWeight: '600',
    color: '#059669',
    textAlign: 'center',
    marginBottom: 10,
  },
  componentText: {
    fontSize: 14,
    color: '#6b7280',
    marginLeft: 10,
  },
  soapText: {
    fontSize: 14,
    color: '#4b5563',
    marginLeft: 10,
    marginBottom: 5,
  },
  interactionCard: {
    backgroundColor: '#fef2f2',
    borderRadius: 8,
    padding: 12,
    marginTop: 10,
    borderLeftWidth: 4,
    borderLeftColor: '#ef4444',
  },
  interactionDrugs: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1f2937',
  },
  interactionText: {
    fontSize: 14,
    color: '#4b5563',
    marginTop: 4,
  },
  severity: {
    fontSize: 12,
    color: '#f59e0b',
    marginTop: 4,
    fontWeight: '600',
  },
  severityHigh: {
    color: '#ef4444',
  },
  noInteractions: {
    fontSize: 14,
    color: '#059669',
    textAlign: 'center',
    marginTop: 10,
  },
  infoCard: {
    backgroundColor: '#eff6ff',
    borderRadius: 12,
    padding: 20,
    marginTop: 20,
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1e40af',
    marginBottom: 8,
  },
  infoText: {
    fontSize: 14,
    color: '#3b82f6',
    lineHeight: 20,
  },
  noData: {
    fontSize: 16,
    color: '#9ca3af',
    textAlign: 'center',
    marginVertical: 20,
  },
  hint: {
    fontSize: 12,
    color: '#9ca3af',
    textAlign: 'center',
  },
});
