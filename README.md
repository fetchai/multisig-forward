# Fetch x Forward

This repo contains the code and workings of the cosmos-sdk native multisig wallet.

## Overview

Address: `fetch1z75gmchl4nx5hacnxj2ck2hg9czwa6ahy2a30z`

## Key Addresses

**Fetch**

Address: `fetch1cj8tsezsej7ltedefnt7cnhwsg0per2ptlam59`

Public Key: `'{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A63MPDxjigrq7t2ceB+U6jyJRJK+C6c3XDxYycD6/fqY"}'`

**Forward**

Address: `fetch19zmc8hah2kcw3rsfup4e0ha979uqa06t7ln37k`

Public Key: `'{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"Ap0VelVvzlRh1AYqEvCOH0j4cWFCoTD7FcuU+wdH7aC2"}'`



## Setup

Run the following commands to import all the key addresses and to build the multisig wallet address


### Step 1. Offline key references

Before building the multisig you need to add references to all the other public keys. Below is the list of keys with some example names

#### First, import your own key using your Ledger HW wallet

This must be done individually — each owner of Ledger HW wallet can import only her/his own Ledger HW.

Importing keys of **OTHER** parties (signatories) is described in the
[Import keys belonging to **OTHER** parties(signatories)](#import-keys-belonging-to-other-parties-signatories)
section below.

Please connect your own Ledger HW wallet to your computer via USB, and execute **ONE** of the following commands — please
select the one with the name of **your** key:
> This is relevant only for advanced users: **IF** you do **not** understand what is this section about,
> you do not need to worry about it, just skip to the commands below.
> 
> The `--account 0` and `--index 0` parameters in command below are the default values, and most people simply use these.
>
> **HOWEVER**, **IF** you used different values for `account` and `index` segments in HD derivation path to derive
> your own key, then please change these values in commandline below.

```
# For "forward" Ledger HW wallet:
fetchd keys add forward --account 0 --index 0 --ledger
```

```
# For "hledgern2" Ledger HW wallet:
fetchd keys add hledgern2 --account 0 --index 0 --ledger
```

#### Import keys belonging to **OTHER** parties (signatories) 
```
# add all the keys into the keyring

# Forward key:
fetchd keys add forward --pubkey '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"Ap0VelVvzlRh1AYqEvCOH0j4cWFCoTD7FcuU+wdH7aC2"}'

# Fetch key:
fetchd keys add hledgern2 --pubkey '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A63MPDxjigrq7t2ceB+U6jyJRJK+C6c3XDxYycD6/fqY"}'
```

`fetchd` will not allow you to add the same key under different names, therefore, typically the command above with corresponds to your name will fail

### Step 2. Build multisig key

Once all the keys are present in your keyring, you can run the following command to create the multisig key

```
# Generate the multisig account in your 'fetchd' keyring:
fetchd keys add multisig-forward --multisig 'hledgern2,forward' --multisig-threshold 2
```

***Note***: You will need to adjust the names in the command to match the values in your keyring

**Verify** that the address matches the one at the top of the README file.

```
- name: multisig-forward
  type: multi
  address: fetch1z75gmchl4nx5hacnxj2ck2hg9czwa6ahy2a30z
  pubkey: '{"@type":"/cosmos.crypto.multisig.LegacyAminoPubKey","threshold":2,"public_keys":[{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"Ap0VelVvzlRh1AYqEvCOH0j4cWFCoTD7FcuU+wdH7aC2"},{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A63MPDxjigrq7t2ceB+U6jyJRJK+C6c3XDxYycD6/fqY"}]}'
  mnemonic: ""
```

### Step 3. Double check

Since this is important please double check all address and public key references.

