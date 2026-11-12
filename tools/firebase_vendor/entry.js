export { initializeApp } from "firebase/app";
export {
  getAuth, connectAuthEmulator, onAuthStateChanged, createUserWithEmailAndPassword, signInWithEmailAndPassword,
  signInWithPopup, GoogleAuthProvider, sendPasswordResetEmail, sendEmailVerification, updatePassword,
  reauthenticateWithCredential, EmailAuthProvider, signOut
} from "firebase/auth";
export { getFirestore, connectFirestoreEmulator, doc, getDoc, setDoc, collection, getDocs, writeBatch, serverTimestamp, query, orderBy, limit, updateDoc, deleteDoc, increment, addDoc, Timestamp } from "firebase/firestore";
